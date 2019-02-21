#!/usr/bin/env python2.7
#-*- coding: utf-8 -*-

import create
import time

ROOMBA_PORT="/dev/ttyUSB0"
robot = create.Create(ROOMBA_PORT)
robot.toSafeMode()

def roombaDo(action):
    if action == "w":
        print "forth"
        robot.go(10, 0)
    elif action == "s":
        print "back"
        robot.go(-10, 0)
    elif action == "a":
        print "left"
        robot.go(0, 20)
    elif action == "d":
        print "right"
        robot.go(0,-20)
    elif action == "c":
        print "clean"
        robot._write(chr(135))
    else:
        roombaClose()

def roombaClose():
    print "stop"
    robot.go(0,0)
    robot.close()

import socket

HOST = '127.0.0.1'
PORT = 8080

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
print 'no client...'
conn, addr = s.accept()
print 'connected by', addr

while True:
    print 'listening...'
    data = conn.recv(1024)
    if len(data) == 0:
        break
    # conn.send(data)
    print 'received:', data
    roombaDo(data)

conn.close()
roombaClose()

