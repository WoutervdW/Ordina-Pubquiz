FROM tensorflow/tensorflow:latest-gpu-py3

# set a directory for the app
WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy all the files to the container
COPY . .

# install dependencies
RUN pip install --upgrade pip
RUN apt-get update
RUN apt-get install poppler-utils -y
RUN apt-get install -y libsm6 libxext6 libxrender-dev
RUN apt-get update && apt-get install -y tesseract-ocr-all

RUN pip install --no-cache-dir -r requirements.txt

# run the command
#CMD ["python", "./home.py"]

ENV FLASK_APP "home.py"
ENV FLASK_ENV "development"
ENV FLASK_DEBUG True

EXPOSE 5000

CMD flask run --host=0.0.0.0
