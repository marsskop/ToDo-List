FROM python:3.8-alpine

RUN adduser -D todolist

WORKDIR /home/todolist

RUN apk --update --no-cache add python3-dev libffi-dev gcc musl-dev make libevent-dev build-base

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/python -m pip install --upgrade pip
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY app app
COPY migrations migrations
COPY todolist.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP todolist.py

RUN chown -R todolist:todolist ./
USER todolist

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
