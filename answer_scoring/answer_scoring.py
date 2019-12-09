# TODO: way to set questions to be marked manually
from answer_scoring.string_processing import check_correct
from answer_scoring.qa import Category, Question, Answer
import pickle


def get_score(question):
    """
    Calculate the score for the given question
    :param questions: list with objects of type Question
    :return: score based on No of correct answers
    """
    score = 0

    if question.category == Category.STANDARD:
        score += score_standard(question)

    elif question.category == Category.MUSIC:
        score += score_music(question)

    elif question.category == Category.PHOTO:
        score += score_photo(question)

    return score


def score(question):

    score = 0

    for answer, correct_answers in zip(question.answers, question.correct_answer_lists):
        # Grant 1 point if the answer is correct
        if check_correct(answer, correct_answers, question.numerical):
            score += 1

    return


def score_standard(question):
    """
    Return number of points gained for a standard question
    :param question: object of type Question
    :return: score
    """
    #
    score = 0
    max_score = question.max_score
    for answer, correct_answers in zip(question.answers, question.correct_answer_lists):
        # Grant 1 point if the answer is correct
        if check_correct(answer, correct_answers, question.numerical):
            score += 1
    return score if score < max_score else max_score


def score_music(question):
    """
    Return number of points gained for a music question
    :param question: object of type Question
    :return:
    """
    # multiple answers, 2 points

    # artist1 = question.answers[0]
    # artist2 = question.answers[1]
    # Create one list with all correct artists
    score = 0
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

    return score


def score_photo(question):
    """
    Return number of points gained for a photo question
    :param question: Object of type Question
    :return:
    """
    # There can be 1 or two people in a picture
    score = 0
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
