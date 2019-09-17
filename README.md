# Introduction

This first assignment consists on building a pipeline that connects edge computing with the cloud. We are using the jetson TX2 developer kit with a webcam to identify faces, load face images in a queue system and the transfer to a queue broker in the cloud to save images within an ibm bucket (object storage).

# Pipeline

To build the pipeline we used the following technologies:
- Python
- Docker
- Mqtt

The pipelines consists on an edge infrastructure and cloud infrastructure.  All details, scripts and dockerfiles are within the corresponding folder of the proyects.

## Edge infrastructure:

- Hw03 Network: This is a network bridge that allow us to communicate all the containers within this network.

- Face detector: This is a container build with Ubuntu 16.04, python 2.7, and opencv. This container has a python scripts that processes images from a webcam and publish them in a topic called "w251/face_detector". Pickle objects are used to transfer images.

- Mqtt broker: This container is build with Alpine, and Mosquitto (mqtt broker). The mqtt broker acts as a bridge to the cloud broker, once messages are published to the following topic "w251/face_detector", the messages are also published on the cloud bridge.

- Mqtt forwarder: This container is build with Alpine, and Mosquitto client. It may subscribe to the topic "w251/face_detector" and publishes to cloud.

## Cloud infrastructure

- Mqtt broker cloud: This is a container build with Alpine, and mosquitto. All messages published on the edge on "w251/face_detector" and published to this broker also.

- Image to file system: This is a container build with Ubuntu 16.04 and python. A python scripts run to get messages published on the following topic "w251/face_detector", and then the pickle object is parsed and saved to an image file within the buckets (object storage) which is mounted within the cloud filesystem.

- Buket: Using S3FS, we mount the object storage bucket to the filesystem.

## QoS

Within this project a main constraint is the bandwidth, cause we are sending images from an edge device to the cloud and the save to object file also through the network. The volume of images processed is big, cause every movement in front of the camera is processed as a frame and face detection is sent to the cloud. Images received per minute vs images generated could be a measure of quality. It does not matter in this case that some images get lost, but speed could be a mayor concern.

# Build images

## Face detector - Edge

```

mkdir face_detector

cd face_detector

docker build -t face_detector .

```

## Mosquitto broker - Edge

```
cd mqtt_broker
docker build -t alpine_mosquitto_broker_edge .

```

## Mosquitto forwarder - Edge

```
cd mqtt_forwarder

docker build -t alpine_mosquitto_forwarder_edge .

```

## Mosquitto broker - Cloud

```
#Create mosquito broker image
docker build -t alpine_mosquitto_broker_cloud .

# Create folders so as to persist data of container.

mkdir -p /var/mosquitto/logs
mkdir -p /var/mosquitto/data
chmod a+w /var/mosquitto

# Copy config file from repository to root folder
cp mosquitto.config /root/.

```

## Image to File - Cloud

```
docker build -t image_to_file_cloud .

```

# Create network

```
#cloud and Edge

docker network create --driver bridge hw03

```

# Run containers
## Face detector container (ubuntu + python)

```
xhost +

docker run --rm --device=/dev/video1 --network hw03 --privileged -e DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -v /data/w251/hw3/face_detector:/face_detector -ti face_detector bash

cd face_detector

python face_detector.py

```

## Mosquito Broker - Edge

```
docker run -d --name broker --network hw03 -it -p 1883:1883 -p 9001:9001 -v ~/mosquitto/data:/mosquitto/data -v ~/mosquitto/logs:/mosquitto/logs alpine_mosquitto_broker_edge

```

## Mosquito forwarder - Edge

```
docker run --name forwarder --network hw03 -ti alpine_mosquitto_forwarder_edge

```
## Mosquitto broker -  Cloud

```
docker run -d --name broker_cloud --network hw03 -it -p 1883:1883 -p 9001:9001 -v /root/mosquitto.conf:/mosquitto/config/mosquitto.conf -v /var/mosquitto/data:/mosquitto/data -v /var/mosquitto/logs:/mosquitto/logs alpine_mosquitto_broker_cloud

#add user and password

docker exec -it <container_id> /bin/sh

#create user and password

mosquitto_passwd -c /mosquitto/data/passwd face_detector

#testing
#publish on local computer

mosquitto_pub -h 169.50.133.249 -t "w251/face_detector" -m "Testing bridged brokers!" -u face_detector -P w251faces
#subscribe on cloud broker
mosquitto_sub -h localhost -v -t "w251/face_detector"

```

## Image to file - Cloud

```

docker run --rm --network hw03 /data/face_detector:/face_detector -ti image_to_file_cloud bash

```

## Create cloud instance (VS)

```
ibmcloud sl vs create --datacenter=dal09 --domain=fvergara.cloud --hostname=w255 --os=UBUNTU_16_64 --cpu=2 --memory=2048 --billing=hourly --key=1555046
```
