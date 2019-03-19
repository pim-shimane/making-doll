#!/usr/bin/env python
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time
import sys

#args = sys.argv

#print(args)
#path = './test.txt'
#with open(path,mode='w') as f:
 
#    for x in xrange(len(args)):
#        print(args[x])
#        f.write(args[x])

#f.close()

GPIO.setmode(GPIO.BCM)
GPIO.setup(13,GPIO.OUT)

for x in xrange(1):
    GPIO.output(13,True)
    time.sleep(2)
    GPIO.output(13,False)
    time.sleep(2)
GPIO.cleanup()

