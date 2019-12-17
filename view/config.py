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
    team_page.append("De Winnaars")
    team_page.append("De Winnaars")
    page_1_line_number = 28
    page_lines = []
    # We will define all the lines in an array of arrays. The database starts with id 1,
    # so we will define an empty array on the 0 index
    page_lines.append([])
    page_lines.append([])
    # similarly to the answersheet we define an empty line since the database starts with id 1
    page_lines[1].append("")
    page_lines[1].append("team naam: De Winnars")
    page_lines[1].append("vraag antwoord")
    page_lines[1].append("Ronde 1: Eerste en enige ronde")
    page_lines[1].append(1)
    page_lines[1].append(2)
    page_lines[1].append(2)
    page_lines[1].append(2)
    page_lines[1].append(2)
    page_lines[1].append(2)
    page_lines[1].append(3)
    page_lines[1].append(3)
    page_lines[1].append(4)
    page_lines[1].append(5)
    page_lines[1].append(6)
    page_lines[1].append(7)
    page_lines[1].append(7)
    page_lines[1].append(7)
    page_lines[1].append(7)
    page_lines[1].append(7)
    page_lines[1].append(8)
    page_lines[1].append(8)
    page_lines[1].append(8)
    page_lines[1].append(8)
    page_lines[1].append(8)
    page_lines[1].append(9)
    page_lines[1].append(10)
    page_lines[1].append(11)
    page_lines[1].append(12)

    # Here we map which question id the question number belongs to (this should be updated to an extra column in the question)
    question_to_id = {}
    question_to_id["1"] = [5, [2]]
    question_to_id["2"] = [6, [3, 4, 5, 6, 7]]
    question_to_id["3"] = [7, [8, 9]]
    question_to_id["4"] = [8, [10]]
    question_to_id["5"] = [9, [11]]
    question_to_id["6"] = [10, [12]]
    question_to_id["7"] = [11, [13, 14, 15, 16, 17]]
    question_to_id["8"] = [12, [18, 19, 20, 21, 22]]
    question_to_id["9"] = [13, [23]]
    question_to_id["10"] = [14, [24]]
    question_to_id["11"] = [15, [25]]
    question_to_id["12"] = [16, [26]]



