from fuzzywuzzy import fuzz, process
import re


# TODO: check string similarity using fuzzywuzzy (https://www.datacamp.com/community/tutorials/fuzzy-string-python)
# TODO: Remove the entry from the list if it has been checked, to prevent duplicate answers from scoring points.
# TODO: compare numbers as ints
# TODO: get the Question from calculate_score to string comparison for the category to parse the string correctly
#  (numbers in songs should be parsed as strings, in other answers they should probably be parsed as integers)

def check_numerical_value(answer, correct_answer):
    # Completely new code

    # DEPRECATED
    for answer_word in answer.split():  # For every word in the given answer
        try:
            value = int(answer_word)  # Try to convert it to an int
        except ValueError:
            pass  # This word is not an integer, try the next one

        return value == correct_answer
    return False


def check_string(answer, correct_answer):
    answer = preprocess_string(answer)
    correct_answer = preprocess_string(correct_answer)

    # Select the string with the highest matching percentage
    # highest = process.extractOne(answer, correct_answers)
    # correct_answer_list.remove(highest[0])
    return fuzz.WRatio(answer, correct_answer) > 80


def check_correct(answer, correct_answers, numerical):
    """
    Check whether this answer is correct.
    :param answer: string representing the answer.
    :param correct_answers: list of possible correct answers.
    :param numerical: boolean, whether the answer should be a number.
    :return: true if the answer is (close enough to) correct, false otherwise.
    """

    # Option 3: check if there is a common substring, if it is numerical, return True
    for correct_answer in correct_answers:
        # Use regex to get all the numbers and compare those from the given answer to those each of the correct answers
        # for 100% similarity

        # Compare substrings. If a substring is a number and it matches an answer exactly, and the rest of the string
        # is similar enough, return True
        if check_numerical_value(answer, correct_answer):
            return True
            # See if the given answer contains a number that exactly matches one in the correct answers, as well as the
            # rest of the string being similar.

        # If no such number exists, check the answer for string-based similarity to any of the correct answers
        # If there is no numerical value that is wrong, compare the entire string. If it is similar (enough), return
        # True.
        if check_string(answer, correct_answer):
            return True

    # If none of the correct answers were similar to correct answers, return False
    return False


def preprocess_string(answer):
    answer = answer.lower()
    return answer


def compare_strings(answer, correct_answer_list):
    """

    :param answer: string
    :param correct_answer_list: list of strings
    :return: True if the string is similar to one of the correct answers, False otherwise
    """

    # Ratio = fuzz.ratio(Str1.lower(), Str2.lower())
    # Partial_Ratio = fuzz.partial_ratio(Str1.lower(), Str2.lower())
    # Token_Sort_Ratio = fuzz.token_sort_ratio(Str1, Str2)
    # ratios = process.extract(answer, correct_answer_list)

    answer = preprocess_string(answer)
    correct_answer_list = [preprocess_string(correct_answer) for correct_answer in correct_answer_list]

    # Select the string with the highest matching percentage
    highest = process.extractOne(answer, correct_answer_list)
    # correct_answer_list.remove(highest[0])
    return highest[1] > 80
