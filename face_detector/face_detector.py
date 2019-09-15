import numpy as np
import cv2
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


#Connect to mqtt broker
Connected         = False

broker            = "mosquitto"

port              = 1883
user              = "face_detector"
password          = "facew255"
client            = mqtt.Client("Python")
client.on_connect = on_connect

client.username_pw_set(user, password=password)
client.connect(broker, port=port)

client.loop_start()

while Connected != True:    #Wait for connection
    time.sleep(0.1)

#Face classifier
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

#Set video device
cap = cv2.VideoCapture(1)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # We don't use the color information, so might as well save space
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
	cv2.rectangle(gray, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    
        # Display the resulting frame
    cv2.imshow('frame',gray)

    client.publish("w251/faces","IMAGES")
    
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        client.disconnect()
        client.loop_stop()
        break
