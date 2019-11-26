from fuzzywuzzy import process


def preprocess_string(answer):
    answer = answer.lower()
    return answer


def compare_string(answer, correct_answer_list):
    """

    :param answer: string
    :param correct_answer_list: list of strings
    :return: True if the string is similar to one of the correct answers, False otherwise
    """
    # TODO: check string similarity using fuzzywuzzy (https://www.datacamp.com/community/tutorials/fuzzy-string-python)
    # TODO: Remove the entry from the list if it has been checked, to prevent duplicate answers from scoring points.
    # TODO: compare numbers as ints
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