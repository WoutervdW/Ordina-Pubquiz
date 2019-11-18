import re

# TODO: hoe werkt scoring? 1 punt per vraag max, goed of fout? Of: meerdere
#  punten voor sommige vragen, afhankelijk van correctheid?

# The answers come as a list of answers. The answers are in the order of
# questioning. Each answer in the list is a list of Strings, each String
# being a separate word of the answer

# Each correct answer is a list of answers. This list contains one element if
# only one answer is correct, but can contain multiple answers

SCORE = 0


def get_score(answers):
    """

    :param answers: list of answers, each answer a list of strings.
    :return: score based on No of correct answers
    """
    for answer in answers:
        global SCORE
        if check_answer(answer):
            SCORE += 1

    return SCORE


def check_answer(answer):
    """

    :param answer: a list of Strings, consituting a sentence which is the answer to the question.
    :return: True for correct answer, False for false answer.
    """
    correct_answers = read_correct_answers()

    return False


def read_correct_answers():
    # TODO: read correct answers from text file
    correct_answers = ["antwoord1", "antwoord2", "antwoord drie", "antwoord vier"]
    return correct_answers
