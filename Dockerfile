FROM python:3.9.15-slim

LABEL MAINTAINER="Jhonatan Matias Martin <jhonatanmatiasmartin@outlook.es>"

WORKDIR /app

RUN apt-get update && apt-get -y install --no-install-recommends ffmpeg \
&& rm -r /var/lib/apt/lists/*

RUN mkdir cache && chmod 777 cache 

COPY ./requirements.txt requirements.txt

RUN pip install python-telegram-bot==20.0a0

RUN pip install -r requirements.txt

COPY . .

CMD [ "python","src/main.py"]