# Dockerfile

### STAGE 1: BUILD ###
FROM node:12-alpine AS build

## Create app directory ##

## TODO
WORKDIR /opt/app/philosophy-frontend-ui

COPY philosophy-frontend-ui/package.json /opt/app/philosophy-frontend-ui

RUN npm install --silent && \
    npm install --silent --save axios;

COPY philosophy-frontend-ui /opt/app/philosophy-frontend-ui

RUN npm run build

## Change from root user ##
#RUN useradd -ms /bin/bash admin
#USER admin


### STAGE 2: Run ###
FROM nginx:1.17.1-alpine
COPY nginx/default.conf /etc/nginx/conf.d/default.conf
#?? I think i only need the 'philosophy-frontend-ui/'build' folder
COPY --from=build /opt/app/philosophy-frontend-ui/build /usr/share/nginx/html
EXPOSE 80
