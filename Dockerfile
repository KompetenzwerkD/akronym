FROM python:3.7-alpine

WORKDIR /app

COPY . /app

RUN apk add --no-cache jpeg-dev zlib-dev freetype-dev libjpeg-turbo-dev libpng-dev
RUN apk add --no-cache --virtual .build-deps build-base linux-headers \
    && pip install Pillow gunicorn

RUN pip install -r requirements.txt

ENTRYPOINT ["./gunicorn.sh"]
