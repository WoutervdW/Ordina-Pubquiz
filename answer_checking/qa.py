from enum import Enum


class Category(Enum):
    STANDARD = "standard"
    MUSIC = "music"
    PHOTO = "photo"


class Question:
    ID = 0
    category = Category.STANDARD
    correct_answer_lists = None  # List of lists of correct Answers
    answers = None  # List of given Answers
    max_score = 1
    # numerical = False Property indicating if it is a numerical question

    def __init__(self, index, category, correct_answer_lists, answers, max_score=1, numerical=False):
        self.index = index
        self.category = category
        self.correct_answer_lists = correct_answer_lists
        self.answers = answers
        self.max_score = max_score
        # self.numerical = numerical

    # Question can be checked by its own methods?


class Answer:
    text = ""
    numerical = False
    correct = False
    confidence = 0

    def __init__(self, text, numerical=False):
        self.text = text
        self.numerical = numerical
