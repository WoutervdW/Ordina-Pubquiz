FROM python:3.7.0

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
RUN apt-get update
RUN apt-get install poppler-utils -y

COPY requirements.txt /usr/src/app
RUN pip install -r requirements.txt

CMD python ./main.py