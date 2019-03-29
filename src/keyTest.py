import create
import time
ROOMBA_PORT="/dev/ttyUSB0"
robot = create.Create(ROOMBA_PORT)
#robot.printSensors() # debug output

#  wall_fun = robot.senseFunc(create.WALL_SIGNAL) # get a callback for a sensor.
#  print (wall_fun()) # print a sensor value.

robot.toSafeMode()

while True:
    direction = raw_input("h:left j:mae k:back l:right")
    if direction == "j":
        print "mae"
        robot.go(5, 0)
    elif direction == "k":
        print "back"
        robot.go(-5, 0)
    elif direction == "h":
        print "left"
        robot.go(0, 10)
    elif direction == "l":
        print "right"
        robot.go(0,-10)
    else:
        print "stop"
        robot.go(0,0)
        time.sleep(2.0)
        robot.close()
        break

