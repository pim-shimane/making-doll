# Taken from
# https://gist.github.com/thenoviceoof/5465084
# but modified to work on my Roomba 770

import time
import create

ROOMBA_PORT = "/dev/ttyUSB0"

# define silence
r = 30

# map note names in the lilypad notation to irobot commands
c4 = 60
cis4 = des4 = 61
d4 = 62
dis4 = ees4 = 63
e4 = 64
f4 = 65
fis4 = ges4 = 66
g4 = 67
gis4 = aes4 = 68
a4 = 69
ais4 = bes4 = 70
b4 = 71
c5 = 72
cis5 = des5 = 73
d5 = 74
dis5 = ees5 = 75
e5 = 76
f5 = 77
fis5 = ges5 = 78
g5 = 79
gis5 = aes5 = 80
a5 = 81
ais5 = bes5 = 82
b5 = 83
c6 = 84
cis6 = des6 = 85
d6 = 86
dis6 = ees6 = 87
e6 = 88
f6 = 89
fis6 = ges6 = 90

# define some note lengths
# change the top MEASURE (4/4 time) to get faster/slower speeds
MEASURE = 240
23HALF = 240*1.5
HALF = MEASURE/2
Q = MEASURE/4
E = MEASURE/8
Ed = MEASURE*3/16
S = MEASURE/16

MEASURE_TIME = MEASURE/64.

# send song
# [140, num, len, (note, dur)_1, ...]
# durations are multiples of 1/64
# a4 a a f8. c'16 | a4 f8. c'16 a2
# e2 e e f8. c'16 | aes4 f8. c'16 a2
# a'4 a,8. a16 a'4 aes8 g | ges16 f g8 r8 bes, ees4 d8 des
# c16 b c8 r8 f,8 aes4 f8. aes16 | c4 a8. c16 e2
# a4 a,8. a16 a'4 aes8 g | ges16 f g8 r8 bes, ees4 d8 des
# c16 b c8 r8 f,8 aes4 f8. c'16 | a4 f8. c,16 a2
# 40/64 bps
print("send songs...")
# first upload the songs to the irobot...
# Welcometo ようこそじゃぱりパーク!
s.write(ints2str([140, 0, 10,
                  f4,E, e4,E, f4,E, fis4,Q, f4,E,
                  fis4,E, g4,Q, gis4,E, gis4,E, a4,Q, HALF]))
# 今日もどったんばったん大騒ぎ!
s.write(ints2str([140, 1, 9,
                  g4,E, fis4,E, f4,HALF, f4,HALF, ais4,HALF,
                  a4,HALF, f4,HALF, dis4,23HALF, gis4,23HALF, g4,23HALF, fis4,23HALF, g4,HALF]))
# ここ以降はまだ
s.write(ints2str([140, 2, 9,
                  a5,Q, a4,Ed, a4,S, a5,Q, aes5,E, g5,E,
                  ges5,S, f5,S, ges5,S]))
s.write(ints2str([140, 3, 8,
                  r,E, bes4,E, ees5,Q, d5,E, des5,E,
                  c5,S, b4,S, c5,E]))
s.write(ints2str([140, 4, 9,
                  r,E, f4,E, aes4,Q, f4,Ed, aes4,S,
                  c5,Q, a4,Ed, c5,S, e5,HALF]))
# play 2 again
# play 3 again
s.write(ints2str([140, 5, 9,
                  r,E, f4,E, aes4,Q, f4,Ed, c5,S,
                  a4,Q, f4,Ed, c5,S, a4,HALF]))

# once all the songs are uploaded, play them at the right times
# add a little extra time, b/c otherwise cuts off the end
print("play songs...")
s.write(ints2str([141, 0]))
time.sleep(MEASURE_TIME*2.01)

s.write(ints2str([141, 1]))
time.sleep(MEASURE_TIME*2.01)

s.write(ints2str([141, 2]))
time.sleep(MEASURE_TIME*1.26)

s.write(ints2str([141, 3]))
time.sleep(MEASURE_TIME*1.01)

s.write(ints2str([141, 4]))
time.sleep(MEASURE_TIME*1.76)

s.write(ints2str([141, 2]))
time.sleep(MEASURE_TIME*1.26)

s.write(ints2str([141, 3]))
time.sleep(MEASURE_TIME*1.01)

s.write(ints2str([141, 5]))
time.sleep(MEASURE_TIME*1.76)
