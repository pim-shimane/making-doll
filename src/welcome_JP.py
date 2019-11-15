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
MEASURE = 120
nHALF = MEASURE*2/3
HALF = MEASURE/2
Q = MEASURE/4
E = MEASURE/8
Ed = MEASURE*3/12
S = MEASURE/12
MEASURE_TIME = MEASURE/64.

def play_song(robot):
  song1 = [(a5,E),(f5,Q),(c5,E),(c5,Q),(a5,HALF),(r,S),(f5,E),(e5,E),(f5,E),(g5,Q),(f5,E),(g5,E),(a5,Q),(ais5,E),(b5,E),(c6,E)]
  song2 = [(a5,E),(g5,E),(f5,Q),(f5,Q),(d6,Q),(c6,Q),(f5,Q),(d5,Q),(ais5,Q),(a5,Q),(g5,Q),(f5,nHALF)]
  song3 = [(g4,nHALF),(c6,E)]
  song4 = [(f5,E),(gis5,E),(f5,E),(gis5,Q),(f5,E),(gis5,Q),(ais5,E),(ais5,E),(gis5,E),(ais5,Q),(b5,E),(ais5,E),(gis5,E),(fis5,E),(dis5,E),(f5,E)]
  songx = [(g4,nHALF),(c6,E)]
  print("uploading songs")
  robot.setSong( 1, song1 )
  robot.setSong( 2, song2 )
  robot.setSong( 3, song3 )
  robot.setSong( 4, song4 )
  time.sleep(2.0)
  print("playing part 1")
  robot.playSongNumber(1)
  time.sleep(MEASURE_TIME*2.96)
  print("playing part 2")
  robot.playSongNumber(2)
  time.sleep(MEASURE_TIME*3)
  robot.playSongNumber(3)
  time.sleep(MEASURE_TIME)
  son1 = songx
  robot.setSong( 1, song1)
  robot.playSongNumber(4)
  time.sleep(MEASURE_TIME*3.2)
  print("playing part 1")
  robot.playSongNumber(1)
  print("done")

robot = create.Create(ROOMBA_PORT)
robot.toSafeMode()
play_song(robot)
robot.close()
