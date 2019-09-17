FROM ubuntu

# build this: e.g docker build -t motion -f Dockerfile.opencv-mqtt
# to run this container, do:
# on the host:
# make sure you're in the X environment
# xhost +
# docker run --rm --privileged -e DISPLAY -v /tmp:/tmp -ti motion bash
# docker run --rm --device=/dev/video1 --privileged -e DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -v /data/w251/hw3/face_detector:/face_detector -ti face_detector bash

RUN apt update

ENV DEBIAN_FRONTEND=noninteractive

ARG URL=http://169.44.201.108:7002/jetpacks/4.2.1

RUN apt-get update && apt install -y git pkg-config wget build-essential cmake unzip curl


WORKDIR /tmp
# RUN rm *.deb

RUN curl $URL/libopencv_3.3.1-2-g31ccdfe11_arm64.deb  -so libopencv_3.3.1-2-g31ccdfe11_arm64.deb
RUN curl $URL/libopencv-dev_3.3.1-2-g31ccdfe11_arm64.deb -so libopencv-dev_3.3.1-2-g31ccdfe11_arm64.deb
RUN curl $URL/libopencv-python_3.3.1-2-g31ccdfe11_arm64.deb -so libopencv-python_3.3.1-2-g31ccdfe11_arm64.deb

RUN apt install -y  libtbb-dev libavcodec-dev libavformat-dev libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libgtk2.0-dev
RUN apt install -y libswscale-dev libv4l-dev
RUN dpkg -i *.deb



RUN apt install -y libcanberra-gtk-module libcanberra-gtk3-module libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev


RUN apt install -y python-pip vim-tiny mosquitto-clients
RUN pip install numpy
RUN pip install paho-mqtt


WORKDIR /

#CMD ["python", "face_detector.py"]
