FROM python:3.8-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app/

COPY requirements.txt .
COPY . .

RUN pip install --upgrade pip && pip install -r requirements.txt
RUN python create_db.py
CMD python main.py
