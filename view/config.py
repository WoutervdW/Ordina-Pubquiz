import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # print("Config")
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

    ANSWERSHEETS_PER_PAGE = 2
    LINES_PER_PAGE = 20
    WORDS_PER_PAGE = 20


class InputConfig:
    # For now we will define each answersheet by hand. This should be done in the front end.
    page_count = 7
    page_1_line_number = 28
    page_1_team = "De ijsvogels"
    page_1_lines = []
    page_1_lines.append("team naam: De ijsvogels")
    page_1_lines.append("Ronde 5")
    page_1_lines.append("Ronde 5: Muziek")
    page_1_lines.append(41)
    page_1_lines.append(41)
    page_1_lines.append(42)
    page_1_lines.append(42)
    page_1_lines.append(43)
    page_1_lines.append(43)
    page_1_lines.append(44)
    page_1_lines.append(44)
    page_1_lines.append(45)
    page_1_lines.append(45)
    page_1_lines.append(46)
    page_1_lines.append(47)
    page_1_lines.append(48)
    page_1_lines.append(49)
    page_1_lines.append(50)
    page_1_lines.append("Ronde 6: Topografische slang")
    page_1_lines.append(51)
    page_1_lines.append(52)
    page_1_lines.append(53)
    page_1_lines.append(54)
    page_1_lines.append(55)
    page_1_lines.append(56)
    page_1_lines.append(57)
    page_1_lines.append(58)
    page_1_lines.append(59)
    page_1_lines.append(60)


