Application is deployed in production via Docker

see folder philosophy-frontend-ui for application code

commands:
$> docker build --tag philosophy/frontend-ui:0.1 .

to run:
$>docker run -d -p 3000:3000 \
   philosophy/frontend-ui:0.1

to attach:
$>docker run -it -p 3000:3000 \
   philosophy/frontend-ui:0.1
