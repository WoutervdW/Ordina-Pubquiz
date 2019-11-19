from fuzzywuzzy import fuzz


# TODO: way to set questions to be marked manually


def get_score(answers):
    """

    :param answers: list of answers, each answer a list containing the answer(s) to the question.
    :return: score based on No of correct answers
    """

    score = 0
    correct_answers, categories = read_correct_answers()

    for answer, correct_answer_list, category in zip(answers, correct_answers, categories):
        if category == "standard":
            score += score_standard(answer, correct_answer_list)
        elif category == "music":
            # TODO: error handling for wrong(ly formatted) answers
            score += score_both_correct([answer[0], answer[1]], [correct_answer_list[0], correct_answer_list[1]])
            score += score_standard([answer[2]], [correct_answer_list[2]])
        elif category == "photo":
            score += score_standard([answer[0]])
            score += score_standard([answer[1]])

    return score


def score_standard(answer, correct_answer_list):
    """
    Score a standard question. If the answer is correct, the participant gets 1 point.
    :param answer:
    :param correct_answer_list:
    :return:
    """
    for correct_answer in correct_answer_list:
        if check_strings(answer, correct_answer):
            return 1
    return 0


def score_both_correct(answer, correct_answer_list):
    pass


def check_strings(answer, correct_answer):
    return False


def read_correct_answers():
    """

    :return:
    """
    # TODO: read correct answers from text file / database
    correct_answers = [["Mr. Bean", "Shrek"], ["400 keer"], ["Mini"], ["Ronnie Flex", "Frenna", "Energie"]]
    categories = ["photo", "standard", "standard", "music"]
    return correct_answers, categories


if __name__ == "__main__":
    answers = [["Mr Bean", "Shrek"],  # FOTO question
               ["400 x"],  # ALGEMEEN question
               ["Mini"],  # FILM & TELEVISIE question
               ["Ronnie Flex", "Frenna", "Energie"]]  # MUZIEK question

    print(get_score(answers))
