# Getting to Philosophy

## Backstory:
https://en.wikipedia.org/wiki/Wikipedia:Getting_to_Philosophy problem. Basically, 97% of the wiki articles can be traced to the “Philosophy” article.

## Application:
TODO coming soon

## Goal:
Build a full-stack app that takes a Wikipedia title as input, and display the path taken from clicking the first link of each page until you get to the Philosophy article.

## Technical Details:
Front-end : ReactJS
Back-end  : Django
Deployment: Docker containers
Notable tech: Python, Javascript, Celery, ActiveMQ, MongoDB

## Deployment
This application needs some environment variables set to work properly. They
cm be set in the operation system or via the file ./.env.

Some variables like *"APP_SERVER_PORT"* are hard coded and need to
be updated in other places, if updated.

The following variables need to be set:

* DJANGO_BENTO_MONGO_SERVER_URL
  * example: "mongodb+srv://{username}:{password}@{mongo_url}?{options}"
* DJANGO_BENTO_BROKER_URL
  * example: "amqp://{username}:{password}@{queue_url}"
* DJANGO_BENTO_CELERY_BROKER_URL
  * example: "amqp://{username}:{password}@{queue_url}"
  * can be the same as *"DJANGO_BENTO_BROKER_URL"*

$> docker-compose up --build

Then go to: localhost:3000


## TODO:
- convert to python 3.X
- make visualization prettier
- deploy application
- display progress metrics
- continuous testing job ~ run monthly
- remove single point of failure in threading, make more than one master
