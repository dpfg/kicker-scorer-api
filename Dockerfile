FROM busybox

MAINTAINER Aliaksandr Ch <xander.blr@gmail.com>

RUN mkdir -p /code/api

COPY . /code/api

RUN chmod +x /code/api/prepare.sh

VOLUME ["/code/api"]
