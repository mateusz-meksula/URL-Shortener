FROM python:3.11-alpine

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install -r requirements.txt --no-cache-dir

COPY ./app /code/app
