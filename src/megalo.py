import time
import create

ROOMBA_PORT = "/dev/ttyUSB0"

# define silence
r = 30

# map note names in the lilypad notation to irobot commands
b3 = 59
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
nHALF = MEASURE*2/3
HALF = MEASURE/2
nHALF = MEASURE*2/3
HALF = MEASURE/2
Q = MEASURE/4
E = MEASURE/8
Ed = MEASURE*3/12
S = MEASURE/12
MEASURE_TIME = MEASURE/64.

def play_song(robot):
  song1 = [(d4,E),(d4,E),(d5,E),(r,S),(a4,E),(r,E),(ais4,E),(g4,E),(f4,Q),(d4,E),(f4,E),(g4,E)]
  song2 = [(c4,E),(c4,E),(d5,E),(r,S),(a4,E),(r,E),(ais4,E),(g4,E),(f4,Q),(d4,E),(f4,E),(g4,E)]
  song3 = [(b3,E),(b3,E),(d5,E),(r,S),(a4,E),(r,E),(ais4,E),(g4,E),(f4,Q),(d4,E),(f4,E),(g4,E)]
  song4 = [(f4,Q),(f4,E),(f4,E),(r,S),(f4,Q),(f4,E),(d4,E),(d4,E),(r,HALF)]
  song5 = [(f4,Q),(f4,E),(f4,E),(r,S),(g4,Q),(ais4,E),(ais4,E),(g4,E),(r,S),(f4,E),(g4,E),(r,HALF)
  song6 = [(f4,Q),(f4,E),(f4,E),(g4,Q),(ais4,Q),(ais4,Q),(c5,Q),(a4,HALF),(d5,Q),(d5,S),(d5,E),(a4,E),(d5,E),(c5,E),(c5,S)]
  print("uploading songs")
  robot.setSong( 1, song1 )
  robot.setSong( 2, song2 )
  robot.setSong( 3, song3 )
  robot.setSong( 4, song4 )
  robot.setSong( 5, song5 )
  robot.setSong( 6, song6 )
  time.sleep(2.0)
  print("playing part 1")
  robot.playSongNumber(1)
  time.sleep(MEASURE_TIME*2.96)
  print("playing part 2")
  robot.playSongNumber(2)
  time.sleep(MEASURE_TIME*3)
  robot.playSongNumber(3)
  time.sleep(MEASURE_TIME*3)
  robot.playSongNumber(4)
  time.sleep(MEASURE_TIME*3)
  robot.playSongNumber(5)
  time.sleep(MEASURE_TIME*3)
  robot.playSongNumber(6)
  time.sleep(MEASURE_TIME*3)
print("done")

robot = create.Create(ROOMBA_PORT)
robot.toSafeMode()
play_song(robot)
robot.close()
