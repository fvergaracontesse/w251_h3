import numpy as np
import paho.mqtt.client as mqtt
import time

#Create mqtt functions
def on_connect(client, userdata, flags, rc):
 
    if rc == 0:
 
        print("Connected to broker")
 
        global Connected                #Use global variable
        Connected = True                #Signal connection 
 
    else:
 
        print("Connection failed")

def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)


#Connect to mqtt broker
Connected         = False

broker            = "broker_cloud"

port              = 1883
user              = "face_detector"
password          = "facew255"
client            = mqtt.Client("Python")
client.on_connect = on_connect

client.loop_start()

client.subscribe("w251/face_detector")

time.sleep(4)

client.loop_stop()




