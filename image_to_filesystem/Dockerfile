#FROM ubuntu
FROM ubuntu

# build this: e.g docker build -t motion -f Dockerfile.opencv-mqtt
# to run this container, do:
# on the host:
# make sure you're in the X environment
# xhost +
# docker run --rm --privileged -e DISPLAY -v /tmp:/tmp -ti motion bash
# docker run --rm --device=/dev/video1 --privileged -e DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -v /data/w251/hw3/face_detector:/face_detector -ti face_detector bash

RUN apt update

WORKDIR /tmp
# RUN rm *.deb

RUN apt install -y python-pip vim-tiny mosquitto-clients
RUN pip install numpy
RUN pip install paho-mqtt


WORKDIR /

#RUN apt install -y python-pip vim-tiny mosquitto-clients libopencv-dev
#RUN pip install --upgrade pip
#RUN pip install opencv-python
#RUN pip install opencv-contrib-python
#RUN pip install paho-mqtt
#RUN pip install numpy

#RUN apt-get install python3-pip
#RUN pip3 install opencv-python
#RUN pip3 install paho-mqtt
#RUN pip3 install numpy


#WORKDIR /

#CMD ["python", "images_to_filesystem.py"]
