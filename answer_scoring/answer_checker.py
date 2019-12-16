from fuzzywuzzy import fuzz, process
import re
from collections import Counter


# TODO: check string similarity using fuzzywuzzy (https://www.datacamp.com/community/tutorials/fuzzy-string-python)
# TODO: Remove the entry from the list if it has been checked, to prevent duplicate answers from scoring points.
# TODO: compare numbers as ints
# TODO: get the Question from calculate_score to string comparison for the category to parse the string correctly
#  (numbers in songs should be parsed as strings, in other answers they should probably be parsed as integers)


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


def check_numerical_values_old(answer, correct_answer, percentage_off=0):
    """
    Get all the numbers from the answer strings and append them to each other. Convert this to a number. These must be
    the same in both the given and correct answer
    :param answer: one string containing the given answer
    :param correct_answer: one string containing a correct answer
    :param percentage_off: percentage the answer can be off from the correct answer
    :return: True if similar, False otherwise
    """

    # Use regex to get all the numbers and compare those from the given answer to those each of the correct answers
    # for 100% similarity

    all_digits_pattern = re.compile(r'\d+')  # get all individual numbers
    answer_values = all_digits_pattern.findall(answer)  # Find all numbers in the answer
    correct_answer_values = all_digits_pattern.findall(correct_answer)  # Find all numbers in the correct answer

    all_chars_pattern = re.compile(r'\D+')  # Get all non-number characters
    answer_chars = all_chars_pattern.findall(answer)
    correct_answer_chars = all_chars_pattern.findall(correct_answer)

    if len(answer_values) == 0 and len(correct_answer_values) == 0:
        # No numbers in answer or correct answer
        return None

    answer_value = int(''.join(map(str, answer_values)))  # concatenate all numbers in the answer
    correct_answer_value = int(''.join(map(str, correct_answer_values)))  # concatenate all numbers in the answer

    # Compare the lists of numbers for any differences in the number of elements
    difference = list((Counter(correct_answer) - Counter(answer)).elements())
    if len(difference) == 0:
        pass

    # Compare substrings. If a substring is a number and it matches an answer exactly, and the rest of the string
    # is similar enough, return True

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


def preprocess_string(answer):
    answer = answer.lower()
    return answer


def check_correct(answer, correct_answers, numerical):
    """
    Check whether this answer is correct.
    :param answer: string representing the answer.
    :param correct_answers: list of possible correct answers.
    :param numerical: boolean, whether the answer should be a number.
    :return: true if the answer is (close enough to) correct, false otherwise.
    """

    # Divide string into numbers (=every substring that can be converted to a number) and strings, and compair them
    # pairwise BUT need to consider the entire string as well

    for correct_answer in correct_answers:
        # number_correct has to be True if the number exists and is correct, False if the number exists but isn't
        # correct and None if no number exists
        number_correct = None
        if numerical:
            number_correct = check_numerical_values(answer, correct_answer)  # Number-based comparison

        if number_correct is None:
            if check_string(answer, correct_answer):  # String-based comparison
                return True
        else:
            if number_correct:
                return True

            # See if the given answer contains a number that exactly matches one in the correct answers, as well as the
            # rest of the string being similar.

        # If no such number exists, check the answer for string-based similarity to any of the correct answers
        # If there is no numerical value that is wrong, compare the entire string. If it is similar (enough), return
        # True.
        # if check_string(answer, correct_answer):
        #    return True

    # If none of the correct answers were similar to correct answers, return False
    return False


def compare_strings(answer, correct_answer_list):
    """
    OLD
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