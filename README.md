# Introduction

# Project Structure

# Install docker

```
sudo apt-get update
sudo apt install docker.io

```

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

## Mosquito Broker - Cloud

```

docker run -p 1883:1883 -p 9001:9001 -v mosquitto.conf:/mosquitto/config/mosquitto.conf -v /data:/mosquitto/data -v /logs:/mosquitto/logs -ti alpine_mosquitto_broker_cloud
docker run -d -it -p 1883:1883 -p 9001:9001 -v /root/mosquitto.conf:/mosquitto/config/mosquitto.conf -v /var/mosquitto/data:/mosquitto/data -v /var/mosquitto/log:/mosquitto/log alpine_mosquitto_broker_cloud

```
