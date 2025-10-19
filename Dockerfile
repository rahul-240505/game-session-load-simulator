FROM python:3.11-slim

RUN apt-get update && apt-get install -y build-essential pkg-config default-libmysqlclient-dev && apt-get clean

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY backend/requirements.txt /app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./backend /app/