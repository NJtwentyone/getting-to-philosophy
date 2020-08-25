#!/usr/bin/env bash
# start-server.sh

# TODO check for envrionment varibales in .env file
cd philosophy-backend-rest
gunicorn philosophyrest.wsgi:application --bind 0.0.0.0:5000 --workers 2
