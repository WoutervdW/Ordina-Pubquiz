FROM tensorflow/tensorflow:latest-gpu-py3

# set a directory for the app
WORKDIR /usr/src/app

# copy all the files to the container
COPY . .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# run the command
#CMD ["python", "./app.py"]

ENV FLASK_APP "app.py"
ENV FLASK_ENV "development"
ENV FLASK_DEBUG True

EXPOSE 5000

CMD flask run --host=0.0.0.0
