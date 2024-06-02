FROM python:3.12-alpine
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app

RUN apk update && apk add gcc python3-dev musl-dev libffi-dev gettext
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -U pip setuptools
RUN pip install -r requirements.txt
COPY . .
