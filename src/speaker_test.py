# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
import json
import create
import time
ROOMBA_PORT="/dev/ttyUSB1"
robot = create.Create(ROOMBA_PORT)
#robot.printSensors() # debug output

#  wall_fun = robot.senseFunc(create.WALL_SIGNAL) # get a callback for a sensor.
#  print (wall_fun()) # print a sensor value.

robot.toSafeMode()

TOKEN = "token_8u5yCqMJExwPO0lG"
HOSTNAME = "mqtt.beebotte.com"
PORT = 8883
TOPIC = "speaker_test/roomba_test"
CACERT = "mqtt.beebotte.com.pem"

straight = unicode(" ストレート",'utf-8')
back = unicode(" バック",'utf-8')
right = unicode(" ライト",'utf-8')
close = unicode(" クローズ",'utf-8')

def on_connect(client, userdata, flags, respons_code):
    print('status {0}'.format(respons_code))
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode("utf-8"))["data"]
    print(data)

#    while True:
    print "aa"
    if data == straight:
	    robot.go(5, 0)
	    print "mae"
    elif data == back:
	    robot.go(-5, 0)
	    print "back"
    elif data == " Left":
	    robot.go(0, 10)
	    print "left"
    elif data == right:
	    robot.go(0,-10)
	    print "right"
    elif data == close:
	    robot.close()
    else:
	    print "stop"
	    robot.go(0,0)
    time.sleep(2.0)
    robot.go(0,0)
#    robot.close()
	# break

client = mqtt.Client()
client.username_pw_set("token:%s"%TOKEN)
client.on_connect = on_connect
client.on_message = on_message
client.tls_set(CACERT)
client.connect(HOSTNAME, port=PORT, keepalive=60)
client.loop_forever()
