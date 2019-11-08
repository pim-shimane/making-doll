import create
import serial
import time
ROOMBA_PORT="/dev/ttyUSB0"
robot = create.Create(ROOMBA_PORT)
serroomba = serial.Serial(ROOMBA_PORT,115200)
#serroomba.write("\x80\x85")#sleep mode
serroomba.write(chr(137))
#  robot.printSensors() # debug output
#  wall_fun = robot.senseFunc(create.WALL_SIGNAL) # get a callback for a sensor.
#  print (wall_fun()) # print a sensor value.




print "start"
#robot._write(chr(128)) #start
#robot._start()
time.sleep(2.0)
robot.close()
