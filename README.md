# Introduction

# Project Structure

# Build images

## Face detector - Edge

```
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
# Create network

```
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

## Mosquito Broker

```
docker run --name mosquitto --network hw03 -p 1883:1883 -ti alpine_mosquitto_broker_edge

```

## Mosquito forwarder

```
docker run --name forwarder --network hw03 -ti alpine_mosquitto_forwarder

```
## Mosquitto broker -  Cloud

```
docker run -d -it -p 1883:1883 -p 9001:9001 -v /root/mosquitto.conf:/mosquitto/config/mosquitto.conf -v /var/mosquitto/data:/mosquitto/data -v /var/mosquitto/logs:/mosquitto/logs alpine_mosquitto_broker_cloud

#add user and password

docker exec -it <container_id> /bin/sh

#create user and password

mosquitto_passwd -c /mosquitto/data/passwd face_detector

```

## Create cloud instance (VS)

```
ibmcloud sl vs create --datacenter=dal09 --domain=fvergara.cloud --hostname=w255 --os=UBUNTU_16_64 --cpu=2 --memory=2048 --billing=hourly --key=1555046
```
