#!/usr/bin/env python
import serial
import binascii

ser = serial.Serial('/dev/ttyUSB0' , 115200)
ser.write("\x80\x85")
