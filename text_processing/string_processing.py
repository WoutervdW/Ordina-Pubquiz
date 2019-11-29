from fuzzywuzzy import fuzz, process


# TODO: check string similarity using fuzzywuzzy (https://www.datacamp.com/community/tutorials/fuzzy-string-python)
# TODO: Remove the entry from the list if it has been checked, to prevent duplicate answers from scoring points.
# TODO: compare numbers as ints
# TODO: get the Question from calculate_score to string comparison for the category to parse the string correctly
#  (numbers in songs should be parsed as strings, in other answers they should probably be parsed as integers)

def check_numerical_value(answer, correct_value):
    for answer_word in answer.split():  # For every word in the given answer
        try:
            value = int(answer_word)  # Try to convert it to an int
        except ValueError:
            pass  # This word is not an integer, try the next one

        return value == correct_value
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

    if numerical:
        # Check if (part of) the answer can be converted to an integer. Convert the correct answer to integer as
        # well. If so, compare the integer value to the integer value of the correct answer. Else, compare the string
        # to the string versions of the correct answers

        # option1: only numerical value is important, correct_answers only contains single int values for numerical
        # answers
        for correct_answer in correct_answers:  # for each correct answer
            for answer_word in answer.split():  # for each word in the given answer
                # If and int value is found in both the answer and the correct answer, and they are the same,
                # return True
                if check_numerical_value(answer_word, correct_answer):
                    return True
    else:
        for correct_answer in correct_answers:
            if check_string(answer, correct_answer):
                return True
        return False

    # Option 2: don't care what is filled in as correct answer, if it contains a number, it can be compared to the
    # answer, and all the rest will be compared as strings

    for correct_answer in correct_answers:  # For every correct answer
        for correct_answer_word in correct_answer.split():  # For every word in the correct answer
            # if every substring of the given answer matches a number in the correct answer and
            try:
                correct_value = int(correct_answer_word)  # Try to convert it to an int
                if check_numerical_value(answer, correct_value):  # Check if the answer contains this int value
                    return True
                elif check_string(answer, correct_answer):
                    return True
            except ValueError:
                # This word is not an int, try to compare it as a string
                if check_string(answer, correct_answer):
                    return True
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
