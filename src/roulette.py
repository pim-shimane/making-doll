import create
import time
import random

ROOMBA_PORT="/dev/ttyUSB0"
robot = create.Create(ROOMBA_PORT)
#robot.printSensors() # debug output
wall_fun = robot.senseFunc(create.WALL_SIGNAL) # get a callback for a sensor.
#print (wall_fun()) # print a sensor value.
robot.toSafeMode()
cnt = 0
randoms = random.randrange(10,40,2)
robot.go(0,-180)
while cnt < randoms :

    cnt+=1
    time.sleep(0.3)
robot.close()
