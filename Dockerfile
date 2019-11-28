FROM python:3.7.0

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN pip install --upgrade pip
RUN apt-get update
RUN apt-get install poppler-utils -y

COPY requirements.txt /usr/src/app
RUN pip install -r requirements.txt

ENV FLASK_APP "view/home.py"
ENV FLASK_ENV "development"
ENV FLASK_DEBUG True
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=password
ENV POSTGRES_HOST=postgres
ENV POSTGRES_PORT=5432
ENV POSTGRES_DB=ordina-pubquiz

EXPOSE 5000
CMD flask run --host=0.0.0.0
