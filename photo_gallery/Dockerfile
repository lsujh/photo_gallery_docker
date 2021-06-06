FROM python:3.8.3-alpine

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# create the appropriate directories
RUN mkdir /home/app
RUN mkdir /home/app/core
RUN mkdir /home/app/static
RUN mkdir /home/app/media
WORKDIR /home/app

# install psycopg2 dependencies
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql-dev gcc python3-dev musl-dev \
    && apk del build-deps \
    && apk --no-cache add musl-dev linux-headers g++

RUN apk --no-cache add \
    # Pillow dependencies
    freetype-dev fribidi-dev harfbuzz-dev jpeg-dev lcms2-dev openjpeg-dev \
    tcl-dev tiff-dev tk-dev zlib-dev jpeg libjpeg-turbo-dev libjpeg

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

COPY ./entrypoint.sh /home/app/

RUN chmod 774 /home/app/entrypoint.sh

ENTRYPOINT ["/home/app/entrypoint.sh"]