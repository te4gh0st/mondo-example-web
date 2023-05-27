# docker for run flask app
FROM python:3.10.11-slim

RUN mkdir app
COPY . /app
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends tzdata
RUN pip3 install Flask pymongo Flask-PyMongo Flask-Bootstrap
RUN pip3 install gunicorn

ENV TZ=Europe/Moscow
RUN cp /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

EXPOSE 80
CMD ["python3", "-m", "gunicorn", "-w", "2", "-b", "0.0.0.0:80", "--preload", "app:app"]
