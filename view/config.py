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

    CORS_HEADERS = 'Content-Type'
    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ANSWERSHEETS_PER_PAGE = 2
    LINES_PER_PAGE = 20
    WORDS_PER_PAGE = 20
    QUESTIONS_PER_PAGE = 1000
    ANSWERS_PER_PAGE = 3


class InputConfig:
    # For now we will define each answersheet by hand. This should be done in the front end.
    page_count = 7
    # Define which team belongs to which page.
    team_page = []
    team_page.append("Blanco")
    team_page.append("Blanco")
    page_1_line_number = 28

    quiz = []
    quiz.append("")
    quiz.append("team naam: De Winnaars")
    quiz.append("Vraag | Antwoord")
    quiz.append("Ronde 1: Eerste en enige ronde")
    quiz.append(1)
    quiz.append(2)
    quiz.append(2)
    quiz.append(2)
    quiz.append(2)
    quiz.append(2)
    quiz.append(3)
    quiz.append(3)
    quiz.append(4)
    quiz.append(5)
    quiz.append(6)
    quiz.append(7)
    quiz.append(7)
    quiz.append(7)
    quiz.append(7)
    quiz.append(7)
    quiz.append(8)
    quiz.append(8)
    quiz.append(8)
    quiz.append(8)
    quiz.append(8)
    quiz.append(9)
    quiz.append(10)
    quiz.append(11)
    quiz.append(12)

    question_subanswer = {}
    question_subanswer["1"] = [8]
    question_subanswer["2"] = [9, 10, 11, 12, 13]
    question_subanswer["3"] = [16, 17]
    question_subanswer["4"] = [18]
    question_subanswer["5"] = [19]
    question_subanswer["6"] = [20]
    question_subanswer["7"] = [21, 22, 23, 24, 25]
    question_subanswer["8"] = [31, 32, 33, 34, 35]
    question_subanswer["9"] = [38]
    question_subanswer["10"] = [39]
    question_subanswer["11"] = [40]
    question_subanswer["12"] = [41]



