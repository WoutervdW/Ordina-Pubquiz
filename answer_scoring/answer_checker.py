from fuzzywuzzy import fuzz, process
import re
from view.models import Team
from view.models import SubAnswerGiven
from view.models import SubAnswer


# TODO: check string similarity using fuzzywuzzy (https://www.datacamp.com/community/tutorials/fuzzy-string-python)
# TODO: Remove the entry from the list if it has been checked, to prevent duplicate answers from scoring points.
# TODO: compare numbers as ints
# TODO: get the Question from calculate_score to string comparison for the category to parse the string correctly
#  (numbers in songs should be parsed as strings, in other answers they should probably be parsed as integers)

# TODO: get questions from database


def check_correct(answer, correct_answers):
    # number_correct has to be True if the number exists and is correct, False if the number exists but isn't
    # correct and None if no number exists
    for correct_answer in correct_answers:
        number_correct = check_numerical_values(answer, correct_answer)  # Compare numbers in the answer
        if number_correct is None:
            # No number, check correctness based on string-based comparison
            if check_string(answer, correct_answer):
                return True
        else:
            if number_correct:
                # Number correct, see if the rest of the string is also correct.
                # TODO: Combine the correctness of the string and number parts
                return True

    return False


def check_numerical_values(answer, correct_answer):
    """
    Find all numbers in the answer
    :param answer:
    :param correct_answer:
    :return:
    """
    all_digits_pattern = re.compile(r'\d+')  # get all individual numbers
    answer_values = all_digits_pattern.findall(answer)  # Find all numbers in the answer
    correct_answer_values = all_digits_pattern.findall(correct_answer)  # Find all numbers in the correct answer

    if len(correct_answer_values) == 0:
        return None
    elif len(answer_values) != 0 and len(correct_answer_values) != 0:
        answer_value = int(''.join(map(str, answer_values)))  # concatenate all numbers in the answer
        correct_answer_value = int(''.join(map(str, correct_answer_values)))  # concatenate all numbers in the answer
        if answer_value == correct_answer_value:
            return True
    else:
        return False


def check_string(answer, correct_answer):
    answer = preprocess_string(answer)
    correct_answer = preprocess_string(correct_answer)

    # Select the string with the highest matching percentage
    # highest = process.extractOne(answer, correct_answers)
    # correct_answer_list.remove(highest[0])
    return fuzz.WRatio(answer, correct_answer) > 80


def preprocess_string(answer):
    answer = answer.lower()
    return answer


def check_all_answers(db=None):
    print("Checking all answers")
    if db is not None:
        given_answers = SubAnswerGiven.query.all()
        for given_answer in given_answers:
            variants = given_answer.corr_answer.variants
            check_correct(given_answer, variants)