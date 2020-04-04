#!/usr/bin/env python3

import re
import begin
import sys
import math
import time
import mido
import pyaudio
import json
from collections import namedtuple
from enum import Enum

RawNotePlay = namedtuple('RawNotePlay', 'midi_num, sec')
RbNotePlay = namedtuple('RbNotePlay', 'midi_num sec_64')
RbTune = namedtuple('RbTune', 'songs play_seq')

MAX_DURATION = 255
NOTE_RANGE = 31, 127
REST = 0
NOTE_C1 = 24
NOTE_A4 = NOTE_C1 + 3*12 + 9


def note_name(note):
    if note == REST:
        return "_"
    else:
        # octaves and offset from C0
        ocv,val = divmod(note-(NOTE_C1-12), 12)
        return "{}{}".format(
            ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B'][val], 
            ocv)


def note_freq(note):
    # A4 (midi #69) = 440Hz, doubles every octave
    return 440 * (2**(1/12)) ** (note-NOTE_A4)


def tune_to_json(tune, stream):
    json.dump({
        "songs": [
            [
                {
                    "note": play.midi_num,
                    "duration": play.sec_64,
                }
                for play in song
            ]
            for song in tune.songs
         ],
        "play-sequence": tune.play_seq,
    }, stream, indent=2)


def expectation_context(context):
    if len(context) == 0:
        return ""
    return " at {}".format(", ".join("{} {}".format(k,repr(v)) for k,v in context.items()))


def expect_type(typ, val, **context):
    if not isinstance(val, typ):
        raise ValueError("Expected {} got {}{}".format(typ, type(val), expectation_context(context)))
    return val


def expect_key(typ, key, obj, **context):
    expect_type(dict, obj, **context)
    try:
        val = obj[key]
    except KeyError as e:
        raise ValueError('Expected "{}" key, found only {}{}'.format(
            key, ", ".join(repr(k) for k in obj), expectation_context(context))) from e
    return expect_type(typ, val, key=key, **context)


def expect_int(val, mn=None, mx=None, **context):
    expect_type(int, val, **context)
    if mn is not None and val < mn or mx is not None and val > mx:
        if mn is not None and mx is not None and mn == mx:
            msg = "{} value".format(mn)
        else:
            msg = "value in range {}-{}".format(mn if mn is not None else '?', mx if mx is not None else '?')
        raise ValueError("Expected {}, got {}{}".format(msg, repr(val), expectation_context(context)))
    return val


def tune_from_json(stream):
    
    data = json.load(stream)
    songlist = []
    for i,songdef in enumerate(expect_key(list, "songs", data)):
        notelist = []
        for j,playdef in enumerate(songdef):
            note_val = expect_int(
                expect_key(int, "note", playdef, song=i, note=j), 
                mn=0, mx=NOTE_RANGE[1], song=i, note=j)
            if note_val < NOTE_RANGE[0]:
                note_val = 0
            note_dur = expect_int(
                expect_key(int, "duration", playdef, song=i, note=j), 
                mn=0, mx=MAX_DURATION, song=i, note=j)
            notelist.append(RbNotePlay(note_val, note_dur))
        songlist.append(notelist)
    playseq = []
    for n in expect_key(list, "play-sequence", data):
        playseq.append(expect_int(n, mn=0, mx=len(songlist)-1, key="play-sequence"))

    return RbTune(songlist, playseq)


def tune_to_bytes(tune, stream):
    stream.write(bytes([len(tune.songs), len(tune.play_seq)]))
    for i,song in enumerate(tune.songs):
        stream.write(bytes([140, i, len(song)]))
        for play in song:
            stream.write(bytes([play.midi_num, play.sec_64]))    
    for songnum in tune.play_seq:
        stream.write(bytes([141, songnum]))


def expect_byte(stream, mn=None, mx=None, **context):
    b = stream.read(1)
    if len(b) == 0:
        raise ValueError("Unexpected end of stream{}".format(expectation_context(context)))
    return expect_int(b[0], mn, mx, **context)


def tune_from_bytes(stream):
    num_songs = expect_byte(stream, mn=1, section="header", field="num songs")
    play_len = expect_byte(stream, mn=1, section="header", field="play length")
    songs = []
    for i in range(num_songs):
        expect_byte(stream, mn=140, mx=140, section="songs", song=i, field="song command")
        expect_byte(stream, mn=i, mx=i, section="songs", song=i, field="song number")
        num_notes = expect_byte(stream, mn=1, section="songs", song=i, field="song length")
        notes = []
        for j in range(num_notes):
            note_val = expect_byte(stream, section="songs", song=i, note=j, field="note value")
            if note_val != 0:
                expect_int(note_val, mn=NOTE_RANGE[0], mx=NOTE_RANGE[1], section="songs", 
                           song=i, note=j, field="note value")
            note_dur = expect_byte(stream, section="songs", song=i, note=j, field="note duration")
            notes.append(RbNotePlay(note_val, note_dur))
        songs.append(notes)
    playseq = []
    for i in range(play_len):
        expect_byte(stream, mn=141, mx=141, section="play sequence", pos=i, field="play command")
        song_num = expect_byte(stream, mn=0, mx=num_songs-1, section="play sequence", pos=i, field="song number")
        playseq.append(song_num)
    return RbTune(songs, playseq)
    

# https://stackoverflow.com/a/974291
def playback_frames_gen(tune, sample_rate):

    for songnum in tune.play_seq:
        for play in tune.songs[songnum]:
    
            #print("{} ".format(note_name(play.midi_num)), end="",flush=True)        
            nsamples = int(sample_rate * play.sec_64 / 64.0)
            
            if play.midi_num == REST:
                for i in range(nsamples): yield 0x80
            else:
                frequency = note_freq(play.midi_num)
                # sine wave sample n
                s = lambda n: math.sin(2 * math.pi * frequency * n / sample_rate)
                for i in range(nsamples): yield int(s(i) * 0x7f + 0x80)
       

def play_tune(tune):

    SAMPLE_RATE = 22050
    CHUNK_FRAMES = 1024

    p = pyaudio.PyAudio()    
    try:
        #for i in range(p.get_device_count()):
        #    print(p.get_device_info_by_index(i)['name'])
        stream = p.open(format=p.get_format_from_width(1), channels=1, rate=SAMPLE_RATE, output=True)
        try:
            frames = playback_frames_gen(tune, SAMPLE_RATE)

            stopping = False    
            while not stopping:
                chunk = []
                for i in range(CHUNK_FRAMES):
                    try:
                        chunk.append(next(frames))
                    except StopIteration:
                        chunk.append(0x80)
                        stopping = True
                stream.write(bytes(bytearray(chunk)))
            
            stream.stop_stream()
        finally:
            stream.close()
    finally:
        p.terminate()


def expect_match(val, pattern, **context):
    m = re.match(pattern, expect_type(str, val, **context))
    if m is None:
        raise ValueError('Invalid format: "{}"{}'.format(val, expectation_context(context)))
    return m


def expect_in(val, permitted, **context):
    if val not in set(permitted):
        raise ValueError('Expected one of {}, got {}{}'.format(
                ', '.join(map(str, permitted)), repr(val), expectation_context(context)))
    return val


def raw_noteplays_from_nokia_gen(stream, tempo):

    beatsec = 60.0 / tempo

    notestrings = stream.read().split()
    if len(notestrings) == 0:
        raise ValueError('No notes found')
    
    for i,nstr in enumerate(notestrings):
    
        m = expect_match(nstr, r'^(\d+)(\.)?(?:(-)|(#)?(.)(\d+))$')
        isrest = m.group(3) is not None

        # establish note type - crotchet, quaver, etc and convert to seconds
        dursec = beatsec * 4.0 / int(expect_in(m.group(1), ('1','2','4','8','16','32'), note=i, part='duration'))
        # dotted?
        if m.group(2) is not None:
            dursec *= 1.5

        if isrest:
            note = REST
        else:
            # get note name, convert to semitones from C
            semitone = {
                'c': 0, 'd': 2, 'e': 4, 'f': 5, 'g': 7, 'a': 9, 'b': 11,
            }[expect_in(m.group(5), ('a','b','c','d','e','f','g'), note=i, part='note')]
            # sharp?
            if m.group(4) is not None:
                semitone += 1
            # octave number
            octave = 3 + expect_int(int(m.group(6)), mn=0, note=i, part="octave")
            # midi num
            note = NOTE_C1 + (octave-1)*12 + semitone

        yield RawNotePlay(note, dursec)


def raw_to_rb_noteplays(raw_noteplays, min_note_len, min_rest_len, skip_num, transpose):

    result = []
    quantbrw = 0.0
    toskip = skip_num

    for play in raw_noteplays:

        note = play.midi_num

        if note != REST:
            # transpose        
            tspsd = play.midi_num + transpose
            # silence notes that are out of playable range
            note = tspsd if NOTE_RANGE[0] <= tspsd <= NOTE_RANGE[1] else REST
            
        notesec = play.sec

        # pay back borrowed duration from previous note, if possible
        payback = min(quantbrw, notesec)
        notesec -= payback
        quantbrw -= payback

        # ignore zero-length notes
        if notesec <= 0:
            continue

        # skip leading rests
        if len(result) == 0 and note == REST:
            continue

        # skip intro notes and the rests between them
        if toskip > 0:
            if note != REST:
                toskip -= 1
            continue

        # ignore notes and rests that are too short, adding duration to previous note and replacing it
        if len(result) > 0 and (
                (note != REST and notesec < min_note_len)
                or (note == REST and notesec < min_rest_len) ):
            note = result[-1].midi_num
            notesec = result[-1].sec_64 / 64.0 + notesec
            del(result[-1])

        # round up to 1/64 second, noting amount borrowed from next note
        sec64 = int(math.ceil(notesec * 64.0))
        quanbrw = (sec64 / 64.0) - notesec

        # split into multiple notes if too long
        while sec64 > MAX_DURATION:
            result.append(RbNotePlay(note, MAX_DURATION))
            sec64 -= MAX_DURATION
        result.append(RbNotePlay(note, sec64))

    return result


def raw_noteplays_from_midi_gen(stream, channel, tempo_scale):

    note = REST
    notesec = 0

    midfile = mido.MidiFile(file=stream)
    for msg in midfile:

        notesec += msg.time * (1.0/tempo_scale)

        # midi spec allows notes to be ended by note_off OR 0-velocity note_on
        if msg.type == 'note_on' and msg.velocity > 0:
            tostart = msg.note
            if (channel is None or msg.channel == channel) and tostart > note: # favour higher notes
                yield RawNotePlay(note, notesec)
                note = tostart
                notesec = 0

        elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
            toend = msg.note
            if (channel is None or msg.channel == channel) and toend == note:
                yield RawNotePlay(note, notesec)
                note = REST
                notesec = 0
                
    yield RawNotePlay(note, notesec)


def rb_noteplays_to_tune(noteplays, max_notes, max_songs):
    songlist = []
    itr = iter(noteplays)
    try:
        for i in range(max_songs):
            songlist.append([])
            for j in range(max_notes):
                songlist[-1].append(next(itr))
    except StopIteration: 
        pass
    return RbTune(songlist, tuple(range(len(songlist))))


def stream_from_name(name, binary=False, write=False):
    if name == "-":
        s = sys.stdout if write else sys.stdin
        if binary: 
            s = s.buffer
        return s
    else:
        return open(name, ('w' if write else 'r') + ('b' if binary else ''))


def to_enum(enumtype):
    def fn(v):
        try:
            return enumtype[v.upper()]
        except KeyError as e:
            raise ValueError('"{}" not one of: {}'.format(v, ', '.join(e.name.lower() for e in enumtype))) from e
    return fn


class OutputFormat(Enum):

    JSON = "json"
    BYTES = "bytes"
    
    def __str__(self):
        return self.name.lower()


class InputFormat(Enum):

    JSON = "json"
    BYTES = "bytes"
    MIDI = "midi"
    NOKIA = "nokia"

    def __str__(self):
        return self.name.lower()


class Default:
    def __init__(self, label):
        self.label = label
    def __str__(self):
        return self.label
    def __eq__(self, o):
        return isinstance(o, Default)

DEFAULT = Default("")


@begin.start
@begin.convert(_automatic=True, channel=int, fromfmt=to_enum(InputFormat), tofmt=to_enum(OutputFormat), tempo=float)
def main(
        infile :"file to read",
        tempo :"for nokia: the bpm, for midi: amount to scale by" =Default("120/1.0"),
        keytp :"semitones to transpose nokia/midi by" =0,
        fromfmt :"input format: {}".format(", ".join([f.name.lower() for f in InputFormat])) =InputFormat.MIDI,
        outfile :"file to write output to" ="-",
        tofmt :"output format: {}".format(", ".join([f.name.lower() for f in OutputFormat])) =OutputFormat.JSON,
        channel :"optional channel to filter midi by" =Default("all"), 
        play :"play audio preview of result" =False, 
        notes :"max notes per song" =16, 
        songs :"max songs to create" =1, 
        lenmin :"min length of note to allow, in seconds" =1.0/64,
        restmin :"min length of rest to allow, in seconds" =0.25,
        intro :"number of notes to skip at the start" =0,
    ):
    """Convert music data file to Roomba song definition"""

    # Input
    if fromfmt == InputFormat.MIDI:
        if tempo == DEFAULT: tempo = 1.0
        if channel == DEFAULT: channel = None
        with stream_from_name(infile, binary=True) as stream:
            raw_note_source = raw_noteplays_from_midi_gen(stream, channel, tempo)
            noteplays = raw_to_rb_noteplays(raw_note_source, lenmin, restmin, intro, keytp)
            tune = rb_noteplays_to_tune(noteplays, notes, songs)
            
    elif fromfmt == InputFormat.NOKIA: 
        if tempo == DEFAULT: tempo = 120
        with stream_from_name(infile, binary=False) as stream:
            raw_note_source = raw_noteplays_from_nokia_gen(stream, tempo)
            noteplays = raw_to_rb_noteplays(raw_note_source, lenmin, restmin, intro, keytp)
            tune = rb_noteplays_to_tune(noteplays, notes, songs)
            
    elif fromfmt == InputFormat.JSON:
        with stream_from_name(infile, binary=False) as stream:
            tune = tune_from_json(stream)
            
    elif fromfmt == InputFormat.BYTES:
        with stream_from_name(infile, binary=True) as stream:
            tune = tune_from_bytes(stream)

    # Output
    if tofmt == OutputFormat.JSON:
        with stream_from_name(outfile, binary=False, write=True) as stream:
            tune_to_json(tune, stream)            
            
    elif tofmt == OutputFormat.BYTES:
        with stream_from_name(outfile, binary=True, write=True) as stream:
            tune_to_bytes(tune, stream)

    # Preview
    if play:
        sys.stderr.write("\nPlaying...\n")
        sys.stderr.flush()
        play_tune(tune)
