from fuzzywuzzy import fuzz


# TODO: way to set questions to be marked manually


def get_score(answers):
    """

    :param answers: list of answers, each answer a list containing the answer(s) to the question.
    :return: score based on No of correct answers
    """

    score = 0
    correct_answers, categories = read_correct_answers()

    for answers_list, correct_answers_list in zip(answers, correct_answers):
        score += score_answer(answers_list, correct_answers_list)

    return score


def score_answer(answers_list, correct_answers_list):
    """

    :param answers_list: list of answers to the question (usually one element)
    :param correct_answers_list: list of possible correct answers
    :return: score for the question
    """

    # TODO: Make answer checking robust
    for correct_answer in correct_answers_list:
        pass
        # ratio = fuzz.ratio(answers_list.lower(), correct_answer.lower())
        # partial_ratio = fuzz.partial_ratio(answer.lower(), correct_answer.lower())
        # token_sort_ratio = fuzz.token_sort_ratio(answer, correct_answer)
        # if token_sort_ratio > 90:
        #     return 1

    return 0


def read_correct_answers():
    """

    :return:
    """
    # TODO: read correct answers from text file
    correct_answers = [["Mr. Bean", "Shrek"], ["400 keer"], ["Mini"], ["Ronnie Flex", "Frenna", "Energie"]]
    categories = ["foto", "algemeen", "filmtv", "muziek"]
    return correct_answers, categories


if __name__ == "__main__":
    answers = [["Mr Bean", "Shrek"],  # FOTO question
               ["400 x"],  # ALGEMEEN question
               ["Mini"],  # FILM & TELEVISIE question
               ["Ronnie Flex", "Frenna", "Energie"]]  # MUZIEK question

    print(get_score(answers))
