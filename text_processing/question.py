from text_processing.question_categories import Categories


class Question:
    index = 0
    category = Categories.STANDARD
    correct_answer_lists = []
    answers = []
    numerical = False

    # property indicating it is a numerical question

    def __init__(self, index, category, correct_answer_lists, answers, numerical=False):
        self.index = index
        self.category = category
        self.correct_answer_lists = correct_answer_lists
        self.answers = answers
        self.numerical = numerical

    # Question can be checked by its own methods?
