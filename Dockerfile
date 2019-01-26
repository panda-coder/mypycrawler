FROM ubuntu:18.10

LABEL maintainer="Ercy Moreira Neto <fireball.vb@gmail.com>"

RUN apt-get update
RUN apt-get install -y python3 python3-dev python3-pip nginx uwsgi-core uwsgi-plugin-python3

COPY ./ /app
WORKDIR /app

RUN pip3 install -r requirements.txt

COPY ./nginx.conf /etc/nginx/sites-enabled/default

EXPOSE 5000
CMD service nginx start && uwsgi --ini /app/app/uwsgi.ini

