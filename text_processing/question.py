from text_processing.question_categories import Categories


class Question:
    index = 0
    category = Categories.STANDARD
    correct_answer_lists = []
    answers = []
    # property indicating it is a numerical question

    def __init__(self, index, category, correct_answer_lists, answers):
        self.index = index
        self.category = category
        self.correct_answer_lists = correct_answer_lists
        self.answers = answers
