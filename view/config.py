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
    # Define which team belongs to which page.
    team_page = []
    team_page.append("De IJsvogels")
    team_page.append("De IJsvogels")
    team_page.append("De Spare Rib Express")
    team_page.append("De Spare Rib Express")
    team_page.append("De Spare Rib Express")
    team_page.append("De Spare Rib Express")
    team_page.append("De Spare Rib Express")
    page_1_line_number = 28
    page_lines = []
    # We will define all the lines in an array of arrays where
    page_lines.append([])
    page_lines[0].append("team naam: De ijsvogels")
    page_lines[0].append("Ronde 5: Muziek")
    page_lines[0].append(41)
    page_lines[0].append(41)
    page_lines[0].append(42)
    page_lines[0].append(42)
    page_lines[0].append(43)
    page_lines[0].append(43)
    page_lines[0].append(44)
    page_lines[0].append(44)
    page_lines[0].append(45)
    page_lines[0].append(45)
    page_lines[0].append(46)
    page_lines[0].append(47)
    page_lines[0].append(48)
    page_lines[0].append(49)
    page_lines[0].append(50)
    page_lines[0].append("Ronde 6: Topografische slang")
    page_lines[0].append(51)
    page_lines[0].append(52)
    page_lines[0].append(53)
    page_lines[0].append(54)
    page_lines[0].append(55)
    page_lines[0].append(56)
    page_lines[0].append(57)
    page_lines[0].append(58)
    page_lines[0].append(59)
    page_lines[0].append(60)


