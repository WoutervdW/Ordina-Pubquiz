# TODO: way to set questions to be marked manually
from text_processing.string_processing import check_correct
from text_processing.question_categories import Category
from text_processing.question import Question

import pickle


def get_score(question):
    """
    Calculate the score for the given question
    :param questions: list with objects of type Question
    :return: score based on No of correct answers
    """
    score = 0

    if question.category == Category.STANDARD:  # 1 answer, 1 point
        for answer, correct_answers in zip(question.answers, question.correct_answer_lists):
            # Grant 1 point if the answer is correct
            if check_correct(answer, correct_answers, question.numerical):
                score += 1

    elif question.category == Category.MUSIC:  # multiple answers, 2 points
        # artist1 = question.answers[0]
        # artist2 = question.answers[1]
        # Create one list with all correct artists
        correct_artists = []
        for correct_artist in question.correct_answerlists[: -1]:
            correct_artists += correct_artist  # question.correct_answer_lists[0] + question.correct_answer_lists[1]

        song_title = question.answers[-1]
        correct_song_titles = question.correct_answer_lists[-1]
        # Grant a point if both artists are correct
        if check_correct(artist1, correct_artists, question.numerical) and \
                check_correct(artist2, correct_artists, question.numerical):
            score += 1
        # Grant a point if the song title is correct
        if check_correct(song_title, correct_song_titles, question.numerical):
            score += 1

    elif question.category == Category.PHOTO:
        # There can be 1 or two people in a picture
        for answer, correct_answer in zip(question.answers, question.correct_answer_lists):
            if check_correct(answer, correct_answer, question.numerical):
                score += 1
    return score


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
    with open("data\\given_answers.pickle", "rb") as f1:
        given_answers = pickle.load(f1)

    # with open("data\\categories.pickle", "wb") as f1:
    #   pickle.dump(categories, f1)

    all_correct_answers, categories = read_correct_answers_and_categories()

    questions = []
    for index in range(len(all_correct_answers)):  # Take number of correct answer lists for the amount of questions
        question = Question(index, categories[index], all_correct_answers[index], given_answers[index])
        questions.append(question)

    score = 0
    for question in questions:
        score += get_score(question)
    print(score)
