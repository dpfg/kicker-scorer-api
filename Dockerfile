FROM busybox

MAINTAINER Aliaksandr Ch <xander.blr@gmail.com>

RUN mkdir -p /code/api

COPY . /code/api

VOLUME ["/code/api"]
