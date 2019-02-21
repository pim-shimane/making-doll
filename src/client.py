#!/usr/bin/env python2.7
#-*- coding: utf-8 -*-

import socket

HOST = '127.0.0.1'
PORT = 8080

# Create socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# establish tcp connection
client.connect((HOST, PORT))

# Data send
while True:
    msg = raw_input("a:left w:forth s:back d:right c:clean -> ")
    client.send(msg)

## Data receive
# data = client.recv(4096)

