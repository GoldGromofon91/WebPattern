FROM python:3.8-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app/

COPY requirements.txt .
COPY . .


RUN pip install --upgrade pip && pip install -r requirements.txt

RUN python manage.py makemigrations
RUN python manage.py migrate
RUN python manage.py fill_db
CMD python manage.py runserver 0.0.0.0:8000
