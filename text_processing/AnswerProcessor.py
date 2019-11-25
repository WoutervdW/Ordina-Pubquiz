# TODO: way to set questions to be marked manually
from fuzzywuzzy import fuzz, process


def get_score(all_answers):
    """
    Calculates overall score for the punquiz for a team's answers to the questions
    :param all_answers: list of answers, each nth answer a list containing the answer(s) to the nth question.
    :return: score based on No of correct answers
    """
    score = 0
    all_correct_answers, categories = read_correct_answers_and_categories()

    for answers, correct_answers_lists, category in zip(all_answers, all_correct_answers, categories):
        # TODO: error handling for wrong(ly formatted) answers
        # answers: list of all the answers to the current question
        # correct_answers_lists: list containing, for each answer, a list  with the possible correct answers
        # category: the question category

        if category == "standard":
            # Grant a point if the answer is in the list of correct answers
            # There is only one answer, and one list of correct answers
            score += score_standard(answers, correct_answers_lists)

        elif category == "music":
            # Grant a point if both artists are correct
            # The first two answers are artists, the first two lists are correct artists
            score += score_both_correct(answers[0:2], correct_answers_lists[0:2])

            # Grant a point if the song name is correct
            # The third answer is the song title
            score += score_standard([answers[2]], [correct_answers_lists[2]])

        elif category == "photo":
            score += score_standard([answers[0]], [correct_answers_lists[0]])
            score += score_standard([answers[1]], [correct_answers_lists[1]])

    return score


def score_standard(answer_list, correct_answer_list):
    """
    Score a standard question. for each correct answer (i.e. similar to an answer in the correct answers), the
    participant gets 1 point.
    :param answer: list containing all the answers to 1 question ["",""]
    :param correct_answer_list: list of lists of possible correct answers.[[""],["",""]
    :return: scored points
    """
    score = 0
    for answer, correct_answers in zip(answer_list, correct_answer_list):
        if compare_string(answer, correct_answers):
            score += 1
    return score


def score_both_correct(answer_list, correct_answer_list):
    """

    :param answer_list:
    :param correct_answer_list:
    :return:
    """
    # TODO: currently scores answers if they are similar to ANY answer to this question
    #  (if you fill in one correct answer twice, you still get the point)
    #  Remove the entry from the list if it has been checked. Do this in check_strings

    if score_standard(answer_list[0], correct_answer_list) + score_standard(answer_list[1], correct_answer_list) == 2:
        return 1
    return 0


def compare_string(answer, correct_answer_list):
    """

    :param answer: string
    :param correct_answer_list: list of strings
    :return: True if the string is similar to one of the correct answers, 0 otherwise
    """
    # TODO: check string similarity using fuzzywuzzy (https://www.datacamp.com/community/tutorials/fuzzy-string-python)
    # TODO: Remove the entry from the list if it has been checked, to prevent duplicate answers from scoring points.
    # Ratio = fuzz.ratio(Str1.lower(), Str2.lower())
    # Partial_Ratio = fuzz.partial_ratio(Str1.lower(), Str2.lower())
    # Token_Sort_Ratio = fuzz.token_sort_ratio(Str1, Str2)

    # ratios = process.extract(answer, correct_answer_list)

    # You can also select the string with the highest matching percentage
    highest = process.extractOne(answer, correct_answer_list)
    correct_answer_list.remove(highest[0])
    return 1 if highest[1] > 80 else 0


def read_correct_answers_and_categories():
    """
    :return: A list of the correct answers for each question, as well as its respective category
    """
    # TODO: read correct answers from text file / database
    # correct_answers contains, for each question, a list of answers, and for each answer a list of possible correct
    # strings
    correct_answers = [[["Mr. Bean"], ["Shrek"]], [["400 keer", "400 x", "vierhonderd", "four hundred"]], [["Mini"]],
                       [["Ronnie Flex"], ["Frenna"], ["Energie"]]]
    categories = ["photo", "standard", "standard", "music"]
    return correct_answers, categories


if __name__ == "__main__":
    # given_answers contains, for every question, a list of strings (answers)
    given_answers = [["Mr Bean", "Shrek"],  # FOTO question
                     ["400x"],  # ALGEMEEN question
                     ["Mini"],  # FILM & TELEVISIE question
                     ["Ronnie Flex", "Frenna", "Energie"]]  # MUZIEK question

    print(get_score(given_answers))