import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    print("Config")
    # ...
    # ...
    user = os.environ['POSTGRES_USER']
    password = os.environ['POSTGRES_PASSWORD']
    host = os.environ['POSTGRES_HOST']
    database = os.environ['POSTGRES_DB']
    port = os.environ['POSTGRES_PORT']

    session_type = os.environ['SESSION_TYPE']


    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ANSWERSHEET_PER_PAGE = 2
    ANSWERS_GIVEN_PER_PAGE = 20
    WORDS_PER_PAGE = 20

