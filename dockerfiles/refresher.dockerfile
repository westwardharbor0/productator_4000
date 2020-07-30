FROM python:3.8-alpine

ENV REFRESHER_CONFIG='./confs/productator.conf.json'

WORKDIR /app
COPY . .
RUN chmod 0777 -R /app

RUN apk add --no-cache --virtual .build-deps g++ python3-dev libffi-dev openssl-dev && \
    pip3 install -r requirements.txt uwsgi && \
    apk del .build-deps
RUN apk add --no-cache --update python3

CMD ["python3", "productator/refresher.py"]

