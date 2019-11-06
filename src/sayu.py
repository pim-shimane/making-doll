import create
import time
ROOMBA_PORT="/dev/ttyUSB0"
robot = create.Create(ROOMBA_PORT)
#robot.printSensors() # debug output

#  wall_fun = robot.senseFunc(create.WALL_SIGNAL) # get a callback for a sensor.
#  print (wall_fun()) # print a sensor value.

robot.toSafeMode()

cnt = 0

while cnt < 10000:
    robot.go(0, 40)
    time.sleep(1.5)
    robot.go(0,-40)
    time.sleep(1.5)
    cnt+=1

print "stop"
robot.go(0,0)
time.sleep(2.0)
robot.close()
