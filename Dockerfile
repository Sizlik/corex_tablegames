FROM python:3.12-alpine
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -U pip setuptools
RUN pip install -r requirements.txt
COPY . .
