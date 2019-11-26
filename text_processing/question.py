from text_processing.question_categories import Categories


class Question:
    index = 0
    category = Categories.STANDARD
    answers = []
    correct_answer_lists = []

    def __init__(self, index, category, answers, correct_answer_lists):
        self.index = index
        self.category = category
        self.answers = answers
        self.correct_answer_lists = correct_answer_lists

