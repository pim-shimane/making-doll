import create
import time

ROOMBA_PORT="/dev/ttyUSB0"
robot = create.Create(ROOMBA_PORT)
#robot.printSensors() # debug output
wall_fun = robot.senseFunc(create.WALL_SIGNAL) # get a callback for a sensor.
#print (wall_fun()) # print a sensor value.
robot.toSafeMode()
robot.go(0,100) # spin
#time.sleep(2.0)
robot.close()
