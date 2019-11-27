# TODO: way to set questions to be marked manually
from text_processing.string_processing import compare_string
from text_processing.question_categories import Categories

import pickle


def get_score(answers_per_question, all_correct_answers, categories):
    """
    Calculates overall score for the pubquiz for a team's answers to the questions
    :param answers_per_question: for each question, a list of given answers.
    :param all_correct_answers: for each question, for each answer, a list of possible correct answers.
    :param categories: for each question, the question category
    :return: score based on No of correct answers
    """
    score = 0
    for answers, correct_answer_lists, category in zip(answers_per_question, all_correct_answers, categories):
        # TODO: error handling for wrong(ly formatted) answers
        # answers: list of all the answers to the current question
        # correct_answer_lists: list containing, for each answer, a list  with the possible correct answers
        # category: the question category

        if category == Categories.STANDARD:
            score += get_score_standard(answers, correct_answer_lists)

        elif category == Categories.MUSIC:
            score += get_score_music(answers, correct_answer_lists)

        elif category == Categories.PHOTO:
            score += get_score_photo(answers, correct_answer_lists)

    return score


def get_score_standard(answers, correct_answer_lists):
    # Grant a point if the answer is in the list of correct answers
    # There is only one answer, and one list of correct answers
    score = 0
    answer = ""
    correct_answer_list = []
    try:
        answer = answers[0]
        correct_answer_list = correct_answer_lists[0]
    except IndexError:
        print("Answer is wrongly formatted: standard")
        raise
    score += score_single(answer, correct_answer_list)
    return score


def get_score_music(answers, correct_answer_lists):
    # Grant a point if both artists are correct
    # The first two answers are artists, the first two lists are correct artists
    score = 0
    artists = []
    correct_artists = []
    try:
        artists = answers[0:2]
        correct_artists = correct_answer_lists[0] + correct_answer_lists[1]
    except IndexError:
        print("Answer is wrongly formatted: artists")
        raise
    score += score_both_correct(artists, correct_artists)

    # Grant a point if the song title is correct
    # The third answer is the song title
    song_title = ""
    correct_song_titles = []
    try:
        song_title = answers[2]
        correct_song_titles = correct_answer_lists[2]
    except IndexError:
        print("Answer is wrongly formatted: song title")
        raise
    score += score_single(song_title, correct_song_titles)
    return score


def get_score_photo(answers, correct_answer_lists):
    # Grant a point for each recognized character / person in the photo
    score = 0
    for answer, correct_answer in zip(answers, correct_answer_lists):
        score += score_single(answer, correct_answer)

    return score


def score_single(answer, correct_answers):
    """
    Score one answer (one string). If the answer is correct (i.e. similar to an answer in the correct answers), the
    participant gets 1 point.
    :param answer: list containing string containing the given answer [""]
    :param correct_answers: list of possible correct answers. ["",""]
    :return: scored points
    """
    if compare_string(answer, correct_answers):
        return 1
    return 0


def score_both_correct(answer_list, correct_answer_list):
    # TODO: currently scores answers if they are similar to ANY answer to this question
    #  (if you fill in one correct answer twice, you still get the point)
    #  Remove the entry from the list if it has been checked. Do this in check_strings
    if score_single(answer_list[0], correct_answer_list) + score_single(answer_list[1], correct_answer_list) == 2:
        return 1
    return 0


def read_correct_answers_and_categories():
    """
    :return: A list of the correct answers for each question, as well as its respective category
    """
    # TODO: read correct answers from text file / database
    # correct_answers contains, for each question, a list of answers, and for each answer a list of possible correct
    # strings
    with open("data\\correct_answers.pickle", "rb") as f:
        correct_answers = pickle.load(f)
    with open("data\\categories.pickle", "rb") as f:
        categories = pickle.load(f)

    return correct_answers, categories


if __name__ == "__main__":
    # given_answers contains, for every question, a list of strings (answers)
    with open("data\\given_answers.pickle", "rb") as f:
        given_answers = pickle.load(f)

    all_correct_answers, categories = read_correct_answers_and_categories()
    print(get_score(given_answers, all_correct_answers, categories))

