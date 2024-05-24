FROM python:3.9-alpine

WORKDIR /app/api

ENV FLASK_APP='app.py'

RUN apk update
RUN apk add --no-cache gcc musl-dev linux-headers
RUN apk add pkgconfig mariadb-dev build-base
RUN python3 -m pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt


CMD ["python3", "app.py"]
