FROM python:3.4

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

ADD requirements.txt /usr/src/app/
RUN pip install --no-cache-dir --upgrade -r requirements.txt
