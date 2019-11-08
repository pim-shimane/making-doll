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
MEASURE = 100
HALF = MEASURE/2
Q = MEASURE/4
Ep = MEASURE/8*3
E = MEASURE/8
Ed = MEASURE*3/16
S = MEASURE/16

MEASURE_TIME = MEASURE/64.



def play_starwars(robot):
  otsukai1 = [(c4,HALF), (d4,E), (e4,Q), (f4,Ep), (g4,Q), (a4,E), (b4,Q), (c5,Ep)]
  otsukai2 = [(c5,Q), (b4,Q), (a4,Q), (g4,Q), (f4,Q), (e4,E), (d4,Q), (c4,Ep)]
  print("uploading songs")
  robot.setSong( 1, otsukai1 )
  robot.setSong( 2, otsukai2 )
  robot.setSong( 3, otsukai1 )
  time.sleep(2.0)
  print("playing part 1")
  robot.playSongNumber(1)
  time.sleep(MEASURE_TIME*2.301)
  print("playing part 2")
  robot.playSongNumber(2)
  time.sleep(MEASURE_TIME*2.101)
  print("playing part 1")
  robot.playSongNumber(1)
  time.sleep(MEASURE_TIME*2.301)
  print("playing part 2")
  robot.playSongNumber(2)
  time.sleep(MEASURE_TIME*2.301)
  print("done")

robot = create.Create(ROOMBA_PORT)
robot.toSafeMode()
play_starwars(robot)
robot.close()
