import numpy as np
import paho.mqtt.client as mqtt
import time
import pickle
#import cv2



from PIL import Image 
import datetime

#Create mqtt functions
def on_connect(client, userdata, flags, rc):
 
    if rc == 0:
 
        print("Connected to broker")
 
        global Connected                #Use global variable
        Connected = True                #Signal connection 
 
    else:
 
        print("Connection failed")

def on_message(client, userdata, message):
#    frame = pickle.loads(message.payload, fix_imports=True, encoding="bytes")
#    frame = cv2.imdecode(frame, cv2.COLOR_BGR2GRAY)
#    filename = "faceDetectorBucket/"+datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")+'.jpg'
#    cv2.imwrite(filename, frame)
    print("message received " ,pickle.loads(message.payload.decode("utf-8")))
    filename = "faceDetectorBucket/"+datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")+'.jpg'    
#    cv2.imwrite(filename, pickle.loads(message.payload.decode("utf-8")))

    pil_img = Image.fromarray(pickle.loads(message.payload.decode("utf-8")))
    print(filename) 
    


    pil_img.save(filename)
    print("message received")
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)


#Connect to mqtt broker
Connected         = False

broker            = "broker_cloud"

port              = 1883



#user              = "face_detector"
#password          = "facew255"
client            = mqtt.Client("Python")
client.on_connect = on_connect
client.on_message = on_message
#client.username_pw_set(user, password=password)
client.connect(broker, port=port)
client.loop_start()

client.subscribe("w251/face_detector")

#try:
while True:

    time.sleep(1)
 
#except KeyboardInterrupt:
   # print "exiting"
   # client.disconnect()
   # client.loop_stop()

#time.sleep(4)

#client.loop_stop()




