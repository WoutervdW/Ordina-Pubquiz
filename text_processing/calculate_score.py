# TODO: way to set questions to be marked manually
from text_processing.string_processing import compare_string
from text_processing.question_categories import Categories
from text_processing.question import Question

import pickle


def get_score(questions):
    """

    :param questions: list of questions. each question is an object of type Question
    :return: score based on No of correct answers
    """
    score = 0
    for question in questions:
        if question.category == Categories.STANDARD:
            answer = question.answers[0]
            correct_answer_list = question.correct_answer_lists[0]
            score += score_single(answer, correct_answer_list)

        elif question.category == Categories.MUSIC:
            artists = question.answers[0:2]
            correct_artists = question.correct_answer_lists[0] + question.correct_answer_lists[1]
            score += score_both_correct(artists, correct_artists)

            # Grant a point if the song title is correct
            # The third answer is the song title
            song_title = question.answers[2]
            correct_song_titles = question.correct_answer_lists[2]
            score += score_single(song_title, correct_song_titles)

        elif question.category == Categories.PHOTO:
            for answer, correct_answer in zip(question.answers, question.correct_answer_lists):
                score += score_single(answer, correct_answer)
    return score


def get_score_standard(question):
    # Grant a point if the answer is in the list of correct answers
    # There is only one answer, and one list of correct answers
    score = 0
    answer = question.answers[0]
    correct_answer_list = question.correct_answer_lists[0]
    score += score_single(answer, correct_answer_list)
    return score


def get_score_music(question):
    # Grant a point if both artists are correct
    # The first two answers are artists, the first two lists are correct artists
    score = 0
    artists = question.answers[0:2]
    correct_artists = question.correct_answer_lists[0] + question.correct_answer_lists[1]
    score += score_both_correct(artists, correct_artists)

    # Grant a point if the song title is correct
    # The third answer is the song title
    song_title = ""
    correct_song_titles = []

    song_title = question.answers[2]
    correct_song_titles = question.correct_answer_lists[2]
    score += score_single(song_title, correct_song_titles)
    return score


def get_score_photo(question):
    # Grant a point for each recognized character / person in the photo
    score = 0
    for answer, correct_answer in zip(question.answers, question.correct_answer_lists):
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

    questions = []
    for index in range(len(all_correct_answers)):  # Take number of correct answer lists for the amount of questions
        question = Question(index, categories[index], all_correct_answers[index], given_answers[index])
        questions.append(question)

    print(get_score(questions))
