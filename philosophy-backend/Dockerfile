# Dockerfile

# NOTE don't forget to set DJANGO_BENTO-XXX when running docker

# FROM directive instructing base image to build upon
# TODO look into python:2.7-slim-buster
FROM python:2.7-buster

## Get the latest security ##

RUN apt-get update


## Create app directory ##

RUN mkdir -p /opt/app
RUN mkdir -p /opt/app/pip_cache
RUN mkdir -p /opt/app/philosophy-backend-rest
RUN mkdir -p /opt/app/philosophy-backend-rest/logs

## Change from root user ##
#
#RUN useradd -ms /bin/bash admin
#USER admin

COPY philosophy-backend-rest/requirements.txt start-server.sh /opt/app/
COPY philosophy-backend-rest /opt/app/philosophy-backend-rest/

RUN rm -f /opt/app/philosophy-backend-rest/logs/*

WORKDIR /opt/app/

RUN pip install -r requirements.txt --cache-dir /opt/app/pip_cache

RUN chmod 755 start-server.sh

EXPOSE 5000
STOPSIGNAL SIGTERM
CMD ["/opt/app/start-server.sh"]
