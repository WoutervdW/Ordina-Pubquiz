FROM tensorflow/tensorflow:latest-gpu-py3

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN pip install --upgrade pip
RUN apt-get update
RUN apt-get install poppler-utils -y
RUN apt-get install -y libsm6 libxext6 libxrender-dev
RUN apt-get update && apt-get install -y tesseract-ocr-all

COPY requirements.txt /usr/src/app
RUN pip install -r requirements.txt


