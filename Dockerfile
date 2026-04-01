FROM python:3.8
MAINTAINER Kylin Soong <kylinsoong.1214@gmail.com>

RUN pip install crossplane

VOLUME /etc/nginx

ENTRYPOINT ["crossplane"]
