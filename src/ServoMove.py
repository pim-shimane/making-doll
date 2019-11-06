#!/usr/bin/python
# coding: utf-8
import RPi.GPIO as GPIO
import time
import signal
import sys

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
while cnt < 10000:
    servo.ChangeDutyCycle(12)
    time.sleep(1)

#    servo.ChangeDutyCycle(12.0)
#    time.sleep(0.5)

    servo.ChangeDutyCycle(2.5)
    time.sleep(0.5)
    cnt+=1
GPIO.cleanup()

