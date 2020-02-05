from fuzzywuzzy import fuzz, process
import re
from view.models import SubAnswer, Team
from view.models import Variant, Person, AnswerGiven
from view.models import Question
from view import db


# TODO: check string similarity using fuzzywuzzy (https://www.datacamp.com/community/tutorials/fuzzy-string-python)
# TODO: Remove the entry from the list if it has been checked, to prevent duplicate answers from scoring points.
# TODO: confidence depends on the last variant checked. This is okay for answers that are right in the end, but answers
#  that are marked as wrong will have a confidence based on the last compared variant.
# TODO: check if everywhere correct_ratio >= threshold = True (not correct_ratio > threshold)

def check_correct(answer, correct_answer_variants, threshold, max_conf_incorrect, max_conf_correct):
    """
    Check if string answer is correct given correct answer variants
    """
    # TODO: Use question types for the special cases (multiple choice, interval, standard)

    correct = False
    confidence = 0

    for correct_answer_variant in correct_answer_variants:
        # check if given answer is too short
        if len(correct_answer_variant) / len(answer) >= 2:  # Will sometimes be divided by zero
            correct = False
            confidence = 100
            continue
        # If correct answer is only 1 symbol, take only the last symbol in the given answer
        if len(correct_answer_variant) == 1:
            answer = answer[-1]

        # Compare numbers in the answer
        correct_ratio, confidence = check_numerical_values(answer,
                                                           correct_answer_variant,
                                                           threshold,
                                                           max_conf_incorrect,
                                                           max_conf_correct)
        if correct_ratio is None:
            # No number in given answer, check correctness based on string comparison
            correct_ratio, confidence = check_string(answer, correct_answer_variant, threshold, max_conf_incorrect,
                                                     max_conf_correct)
            correct = correct_ratio >= threshold
            continue

        elif correct_ratio >= threshold:
            # Number correct, see if the rest of the string is also correct.
            # TODO: Combine the correctness of the string and number parts
            correct = True
            continue

        else:
            correct = False
            continue

    return correct, confidence


def check_numerical_values(answer, correct_answer_variant, threshold, max_conf_incorrect, max_conf_correct):
    """
    Find all numbers in the answer
    :param answer: string
    :param correct_answer_variant: string
    :return: None if no number in given answer, True if correct number in given answer, False if incorrect number
    """
    all_digits_pattern = re.compile(r'\d+')  # get all individual numbers
    answer_values = all_digits_pattern.findall(answer)  # Find all numbers in the answer
    correct_answer_values = all_digits_pattern.findall(correct_answer_variant)  # Find all numbers in the correct answer

    # TODO: if the answer (or probably better: the correct answer!) contains both letters and numbers, do letter-based
    #  comparison
    # TODO: improve structure. Still quite expansive for clarity in case of possible functionality changes
    if len(correct_answer_values) == 0:  # no number found in correct_answer
        if len(answer_values) == 0:  # no number found in given_answer
            return None, 0
        else:  # number found in given_answer
            # might be detected wrong, so check string comparison
            return None, 0
    elif len(correct_answer_values) != 0:  # number found in correct answer
        if len(answer_values) == 0:  # no number found in given_answer
            return 0, max_conf_incorrect
        else:  # number found in given_answer
            answer_value = int(''.join(map(str, answer_values)))  # concatenate all numbers in the answer
            correct_answer_value = int(
                ''.join(map(str, correct_answer_values)))  # concatenate all numbers in the answer
            if answer_value == correct_answer_value:
                return 100, max_conf_correct  # confident the answer is correct
            else:
                # might be detected wrong, so check string comparison
                return 0, max_conf_incorrect


def check_string(answer, correct_answer_variant, threshold, max_conf_incorrect, max_conf_correct):
    # TODO: use several different string comparison techniques to get better results and confidence
    # TODO: for a question with multiple answers, if the answers are similar, only remove the most similar answer from
    #  the "already compared" list

    # pre-process strings
    answer = preprocess_string(answer)
    correct_answer_variant = preprocess_string(correct_answer_variant)

    correct_ratio = fuzz.ratio(answer, correct_answer_variant)
    print("Correct ratio: " + str(correct_ratio))
    confidence = calculate_confidence(correct_ratio, threshold, max_conf_incorrect, max_conf_correct)

    return correct_ratio, confidence


def preprocess_string(answer):
    # lower & upper case is handled by fuzz.WRatio
    answer = answer.lower()
    # answer = answer.strip()

    # remove all but \w
    all_word_chars_pattern = re.compile(r'\w+')
    answer = all_word_chars_pattern.findall(answer)  # get all individual letters and numbers sequences
    answer = ''.join(map(str, answer))
    return answer


def calculate_confidence(correct_ratio, threshold, max_conf_incorrect, max_conf_correct):
    # might be improved by using answer length

    # confidence at 100 or 0 correctness should be 100, confidence at threshold should be 0
    # TODO: confidence should likely be lower at 0 correctness, because of reliability of the system
    # TODO: add word-confidence

    # hacky way to solve zero-division errors TODO: Create better way to solve these errors
    if threshold == 0:
        threshold = 1
    if threshold == 100:
        threshold = 99

    if correct_ratio < threshold:
        confidence = max_conf_incorrect - correct_ratio / threshold * max_conf_incorrect
    else:
        confidence = (correct_ratio - threshold) / (max_conf_correct - threshold) * max_conf_correct
    return confidence


def get_variant_lists(question_id):
    # Get the list of all correct subanswers that belong to the same question as the given subanswer
    subanswers = SubAnswer.query.filter_by(question_id=question_id).all()

    # Get all variants for each subanswer and append them into a usable list
    variant_lists = []
    for subanswer in subanswers:
        subanswer_id = subanswer.id
        variants = Variant.query.filter_by(subanswer_id=subanswer_id)
        variants = [variant.answer for variant in variants]
        variant_lists.append(variants)

    return variant_lists


def check_subanswer_given(subanswer_given, subanswers, checker, threshold, max_conf_incorrect, max_conf_correct):
    if subanswer_given.checkedby.personname != 'nog niet nagekeken':
        return  # correct functionality
        # pass  # testing
    print("Read answer: '" + subanswer_given.read_answer + "'")
    if len(subanswer_given.read_answer) == 0:  # no answer: incorrect
        subanswer_given.checkedby = checker
        subanswer_given.correct = False
        subanswer_given.confidence = 100
        return

    correct = False
    confidence_correct = 0
    confidence_false = 100
    most_similar_answer = None  # most similar subanswer

    for subanswer in subanswers:
        variants = [variant.answer for variant in subanswer.variants]  # create usable list for variants
        print("Correct answer variants: " + str(variants))

        correct_temp, confidence_temp = check_correct(subanswer_given.read_answer,
                                                      variants,
                                                      threshold,
                                                      max_conf_incorrect,
                                                      max_conf_correct)

        if correct_temp:
            print("Found similar answer in: " + str(variants))
            correct = True
            if confidence_temp >= confidence_correct:
                confidence_correct = confidence_temp
                most_similar_answer = subanswer
        else:  # not correct
            print("Not similar to: " + str(variants))
            if confidence_temp <= confidence_false:
                confidence_false = confidence_temp

    subanswer_given.checkedby = checker
    subanswer_given.correct = correct
    linereadconfidence = subanswer_given.probability_read_answer
    if subanswer_given.correct:
        subanswer_given.confidence = int(confidence_correct * linereadconfidence)
        subanswers.remove(most_similar_answer)  # this subanswer was already used as a correct option!
    else:
        subanswer_given.confidence = int(confidence_false * linereadconfidence)
    print("Commiting " + str(correct) + " with confidence " + str(subanswer_given.confidence))
    db.session.commit()
    print("")


def iterate_questions(threshold=50, max_conf_incorrect=50, max_conf_correct=100):
    # check each question for its correct answers
    print("Checking all answers")
    checker = Person.query.filter_by(personname="systeem").first()
    questions = Question.query.all()
    for question in questions:
        print("Question " + str(question.questionnumber) + ": " + question.question)
        answers_given_per_team = AnswerGiven.query.filter_by(question_id=question.id).all()  # one per team

        for team_answers in answers_given_per_team:
            if team_answers is None:
                continue  # skip this team's answers
            print("Team: " + Team.query.filter_by(id=team_answers.team_id).first().teamname)
            subanswers_given = team_answers.subanswersgiven
            subanswers = SubAnswer.query.filter_by(question_id=question.id).all()  # one set of subanswers per question

            for subanswer_given in subanswers_given:
                # change threshold based on question type
                check_subanswer_given(subanswer_given,
                                      subanswers,
                                      checker,
                                      threshold,
                                      max_conf_incorrect,
                                      max_conf_correct)

    print("All questions checked")
