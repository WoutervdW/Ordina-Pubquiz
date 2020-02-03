import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    print("Config")
    # ...
    # ...
    user = os.environ.get('POSTGRES_USER') or None
    password = os.environ.get('POSTGRES_PASSWORD') or None
    host = os.environ.get('POSTGRES_HOST') or None
    database = os.environ.get('POSTGRES_DB') or None
    port = os.environ.get('POSTGRES_PORT') or None

    session_type = os.environ.get('SESSION_TYPE') or None

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    CORS_HEADERS = 'Content-Type'
    # SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://localhost/ordina_pubquiz'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ANSWERSHEETS_PER_PAGE = 2
    LINES_PER_PAGE = 20
    WORDS_PER_PAGE = 20
    QUESTIONS_PER_PAGE = 1000
    ANSWERS_PER_PAGE = 3

