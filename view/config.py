import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # ...
    # ...
    user = os.environ['POSTGRES_USER']
    password = os.environ['POSTGRES_PASSWORD']
    host = os.environ['POSTGRES_HOST']
    database = os.environ['POSTGRES_DB']
    port = os.environ['POSTGRES_PORT']


    SQLALCHEMY_DATABASE_URI = f'postgresql://{user}:{password}@{host}:{port}/{database}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False



