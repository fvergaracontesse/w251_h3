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
cd face_detector

docker build -t face_detector .

```

## Mosquito broker - Edge

```
cd mqtt_broker
docker build -t alpine_mosquitto_broker_edge .

```

## Mosquito forwarder - Edge

```
cd mqtt_forwarder

docker build -t alpine_mosquitto_forwarder_edge .

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

## Mosquito Broker - Cloud

```

docker run -p 1883:1883 -p 9001:9001 -v mosquitto.conf:/mosquitto/config/mosquitto.conf -v /data:/mosquitto/data -v /logs:/mosquitto/logs -ti alpine_mosquitto_broker_cloud
docker run -d -it -p 1883:1883 -p 9001:9001 -v /root/mosquitto.conf:/mosquitto/config/mosquitto.conf -v /var/mosquitto/data:/mosquitto/data -v /var/mosquitto/log:/mosquitto/log alpine_mosquitto_broker_cloud

```
