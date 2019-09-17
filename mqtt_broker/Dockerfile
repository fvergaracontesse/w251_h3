FROM alpine:3.9

RUN apk update && \
    apk add --no-cache \
    mosquitto

RUN mkdir -p /mosquitto/logs
RUN mkdir -p /mosquitto/data
RUN chmod a+w /mosquitto

COPY mosquitto.conf /mosquitto/mosquitto.conf

#ENTRYPOINT ["mosquitto -c /mosquitto/mosquitto.conf"]
CMD ["/usr/sbin/mosquitto", "-c", "/mosquitto/mosquitto.conf"]
