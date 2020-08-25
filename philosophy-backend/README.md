Application is deployed in production via Docker

see folder philosophy-backend-rest for application code

commands:
$> docker build --tag philosophy/backend-rest:0.1 .

$>docker run -it -p 5000:5000 \
  -e DJANGO_BENTO_MONGO_SERVER_URL="<MONGO_URL>" \
  -e DJANGO_BENTO_BROKER_URL="<BROKER_URL>" \
  -e DJANGO_BENTO_CELERY_BROKER_URL="<BROKER_URL>" \
   philosophy/backend-rest:0.1 [bin/bash]
