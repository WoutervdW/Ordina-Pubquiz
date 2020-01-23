from fuzzywuzzy import fuzz, process
import re
from view.models import SubAnswerGiven
from view.models import SubAnswer
from view.models import Variant, Person, AnswerGiven
from view import db

import time


# TODO: check string similarity using fuzzywuzzy (https://www.datacamp.com/community/tutorials/fuzzy-string-python)
# TODO: Remove the entry from the list if it has been checked, to prevent duplicate answers from scoring points.
# TODO: confidence depends on the last variant checked. This is okay for answers that are right in the end, but answers
#  that are marked as wrong will have a confidence based on the last compared variant.
# TODO: check if everywhere correct_ratio >= threshold = True (not correct_ratio > threshold)

def check_correct(answer, correct_answer_variants, threshold, max_conf_incorrect, max_conf_correct):
    """

    :param answer: string of given answer
    :param correct_answer_variants: list of strings: variants of correct answer
    :param threshold: The threshold of similarity that must be reached in order to be correct
    :param max_conf_incorrect: max confidence for an incorrect answer
    :param max_conf_correct: max confidence for a correct answer
    :return: correctness (True or False), confidence in decision
    """
    # number_correct has to be True if the number exists and is correct, False if the number exists but isn't
    # correct and None if no number exists
    for correct_answer_variant in correct_answer_variants:
        # TODO: Create categories for these special cases
        # check if given answer is too short
        if len(correct_answer_variant) / len(answer) >= 2:  # Will sometimes be divided by zero
            return False, 100
        # If correct answer is only 1 symbol, take only the last symbol in the given answer
        if len(correct_answer_variant) == 0:
            answer = answer[-1]

        correct_ratio, confidence = check_numerical_values(answer, correct_answer_variant,
                                                           threshold, max_conf_incorrect,
                                                           max_conf_correct)  # Compare numbers in the answer
        if correct_ratio is None:
            # No number in given answer, check correctness based on string comparison
            correct_ratio, confidence = check_string(answer, correct_answer_variant, threshold, max_conf_incorrect,
                                                     max_conf_correct)
            return correct_ratio > threshold, confidence

        elif correct_ratio >= threshold:
            # Number correct, see if the rest of the string is also correct.
            # TODO: Combine the correctness of the string and number parts
            return True, confidence

        else:

            return False, confidence


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

    # pre-process strings
    answer = preprocess_string(answer)
    correct_answer_variant = preprocess_string(correct_answer_variant)

    correct_ratio = fuzz.WRatio(answer, correct_answer_variant)
    confidence = calculate_confidence(correct_ratio, threshold, max_conf_incorrect, max_conf_correct)

    return correct_ratio, confidence


def preprocess_string(answer):
    # lower & upper case is handled by fuzz.WRatio
    # answer = answer.lower()
    return answer


def calculate_confidence(correct_ratio, threshold, max_conf_incorrect, max_conf_correct):
    # might be improved by using answer length

    # confidence at 100 or 0 correctness should be 100, confidence at threshold should be 0
    # TODO: confidence should likely be lower at 0 correctness, because of reliability of the system

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


def check_all_answers(threshold=50, max_conf_incorrect=50, max_conf_correct=100):
    print("Checking all answers")

    # get all given subanswers
    all_subanswers_given = SubAnswerGiven.query.all()
    checker = Person.query.filter_by(personname="systeem").first()

    checked_answers = 0
    start = time.time()
    # check correctness per given answer
    for subanswer_given in all_subanswers_given:
        if subanswer_given.checkedby.personname == 'nog niet nagekeken':
            checked_answers += 1
            subanswer_given.checkedby = checker

            print("Given answer: " + subanswer_given.read_answer)
            if len(subanswer_given.read_answer) == 0:  # Any other reasons to immediately see the answer as False?
                print("incorrect")
                subanswer_given.correct = False
                subanswer_given.confidence = 100
                db.session.commit()
                break
            else:
                # Get the list of all correct subanswers that belong to the same question as the given subanswer
                answergiven = AnswerGiven.query.filter_by(id=subanswer_given.answergiven_id).first()
                question_id = answergiven.question_id
                subanswers = SubAnswer.query.filter_by(question_id=question_id).all()

                # Get all variants for each subanswer and append them into a usable list
                variant_lists = []
                for subanswer in subanswers:
                    subanswer_id = subanswer.id
                    variants = Variant.query.filter_by(subanswer_id=subanswer_id)
                    variants = [variant.answer for variant in variants]
                    variant_lists.append(variants)

                print("Correct answer options: " + str(variant_lists))

            for variants in variant_lists:
                # TODO @wouter: remember checked answers! If an answer occurs twice, the second instance should not be
                #  correct (If the same answer twice is correct, than the "correct answers" should contain two of the
                #  same answer). So, all variants of the first instance should be removed (locally).

                correct, confidence = check_correct(subanswer_given.read_answer,
                                                    variants,
                                                    threshold,
                                                    max_conf_incorrect,
                                                    max_conf_correct)
                if correct:
                    print("Found similar answer in: " + str(variants))
                    subanswer_given.correct = True
                    subanswer_given.confidence = confidence
                    db.session.commit()
                    break
                else:
                    # print("Not similar to: " + str(variants))
                    subanswer_given.correct = False
                    subanswer_given.confidence = confidence
            if subanswer_given.correct:
                print("correct")
            else:
                print("no similar answer found")
    db.session.commit()
    # subanswer_variants_lists.remove(subanswer_variants)

    print("aantal nagekeken subantwoorden: " + str(checked_answers))
    end = time.time()
    print("time elapsed: " + str(end - start))
