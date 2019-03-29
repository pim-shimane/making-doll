"""import create
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
"""

#!/usr/bin/python
# coding: utf-8
import RPi.GPIO as GPIO
import time
import signal
import sys
import create
import time

ROOMBA_PORT="/dev/ttyUSB0"
robot = create.Create(ROOMBA_PORT)
#robot.printSensors() # debug output
#  print (wall_fun()) # print a sensor value.

robot.toSafeMode()

def exit_handler(signal, frame):
    # Ctrl+C push
    print("\nExit")
    servo.ChangeDutyCycle(2.0)
    time.sleep(0.5)
    servo.stop()
    GPIO.cleanup()
    sys.exit(0)

signal.signal(signal.SIGINT,exit_handler)

GPIO.setmode(GPIO.BCM)

gp_out = 4
GPIO.setup(gp_out, GPIO.OUT)
servo = GPIO.PWM(gp_out, 50) 

servo.start(0.0)
cnt = 0
time.sleep(4)
while cnt < 100:
    servo.ChangeDutyCycle(12)
    time.sleep(1)
    servo.ChangeDutyCycle(2.5)
    time.sleep(0.5)
    cnt+=1
    robot.go(0, 1)
    robot.go(0, -1)
time.sleep(2.0)
robot.close()
GPIO.cleanup()
