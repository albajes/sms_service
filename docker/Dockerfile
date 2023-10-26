# pull official base image
FROM python:3.8.3-alpine

# set work directory
WORKDIR /app2

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies
RUN pip install --upgrade pip
COPY /service2/service2/requirements.txt /app2/
RUN pip install -r requirements.txt

ADD /service2/service2 /app2/service2
ADD /service2/docker /app2/docker
ADD /service2/venv /app2/venv

RUN chmod +x /app2/docker/entrypoint.sh
RUN chmod +x /app2/docker/worker-entrypoint.sh