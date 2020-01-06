import unittest
import answer_checking.answer_checker as answer_checker


class AnswerCheckerTest(unittest.TestCase):
    correct_answers = [
        ["Mr. Bean", "Shrek"],
        ["Mr. Bean", "Shrek"],
        ["1980"],
        ["zesenveertig", "zesenveertig meter", "46", "46m", "46 meter"],
        ["1000000", "1 miljoen"]
    ]

    def test_answer_checker(self):
        given_answers = [
            # photo questions
            ["Mr. Bean"],
            ["Shrek"],
            ["1980"],
            ["46 meter"],
            ["1000000"]
        ]
        for given_answer, correct_answer_variants in zip(given_answers, self.correct_answers):
            self.assertTrue(answer_checker.check_correct(given_answer, correct_answer_variants))

