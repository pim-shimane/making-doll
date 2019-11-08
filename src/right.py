import create
import time

ROOMBA_PORT="/dev/ttyUSB0"
robot = create.Create(ROOMBA_PORT)
#robot.printSensors() # debug output
wall_fun = robot.senseFunc(create.WALL_SIGNAL) # get a callback for a sensor.
#print (wall_fun()) # print a sensor value.
robot.toSafeMode()
cnt = 0

#while True :
#    robot.go(100,0) # spin
#    cnt+=1
robot.go(0,-90)
#    time.sleep(0.5)
time.sleep(0.1)
robot.close()
