# TODO: way to set questions to be marked manually
from answer_scoring.answer_checker import check_correct
from answer_scoring.qa import Category, Question, Answer
import pickle


def score_answers_one_by_one(question):
    """
    Grant a point for each answer that is correct
    :param question:
    :return:
    """
    score = 0
    # Each correct answer that is given grants one point
    for correct_answers in question.correct_answer_lists:
        for answer in question.answers:
            if check_correct(answer, correct_answers):
                score += 1
                break  # don't grant any additional point for this answer
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
        score += score_answers_one_by_one(question)
    print(score)
