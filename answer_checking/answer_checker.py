from fuzzywuzzy import fuzz, process
import re
from view.models import SubAnswer, Team
from view.models import Variant, Person, AnswerGiven
from view.models import Question
from view import db


def calculate_confidence(correct_ratio, threshold, max_conf_incorrect, max_conf_correct):
    # hacky way to solve zero-division errors for unusual thresholds
    if threshold == 0:
        threshold = 1
    if threshold == 100:
        threshold = 99

    if correct_ratio < threshold:
        confidence = max_conf_incorrect - (correct_ratio / threshold * max_conf_incorrect)
    else:
        confidence = (correct_ratio - threshold) / (100 - threshold) * max_conf_correct
    return confidence


def preprocess_string(answer):
    # TODO: just remove all characters not found in the correct answer
    answer = answer.lower()
    all_word_chars_pattern = re.compile(r'\w+')  # remove all but numbers and letters
    answer = all_word_chars_pattern.findall(answer)  # get all individual letters and numbers sequences
    answer = ''.join(map(str, answer))
    return answer


def check_string(answer, correct_answer_variant, threshold, max_conf_incorrect, max_conf_correct):
    # TODO: use several different string comparison techniques to get better results and confidence

    # pre-process strings
    answer = preprocess_string(answer)
    correct_answer_variant = preprocess_string(correct_answer_variant)

    correct_ratio = fuzz.ratio(answer, correct_answer_variant)
    print("Correct ratio: " + str(correct_ratio))
    confidence = calculate_confidence(correct_ratio, threshold, max_conf_incorrect, max_conf_correct)

    return correct_ratio, confidence


def check_numerical_values(answer, correct_answer_variant, threshold, max_conf_incorrect, max_conf_correct):
    """
    Find all numbers in the answer
    :param answer: string
    :param correct_answer_variant: string
    :return: None if no number in correct answer, True if correct number in given answer, False if incorrect number
    """
    # TODO: if the answer (or probably better: the correct answer!) contains both letters and numbers, do letter-based
    #  comparison
    # TODO: improve structure. Still quite expansive for clarity in case of possible functionality changes
    all_digits_pattern = re.compile(r'\d+')  # get all individual numbers
    answer_values = all_digits_pattern.findall(answer)  # Find all numbers in the answer
    correct_answer_values = all_digits_pattern.findall(correct_answer_variant)  # Find all numbers in the correct answer

    if len(correct_answer_values) == 0:  # no number found in correct_answer
        return None, 0
    else:  # number found in correct answer
        if len(answer_values) == 0:  # no number found in given_answer
            return 0, max_conf_incorrect / 2
        else:  # number found in given_answer
            # concatenate all numbers in the answer and in the correct answer
            answer_value = int(''.join(map(str, answer_values)))
            correct_answer_value = int(''.join(map(str, correct_answer_values)))
            # if answer_value == correct_answer_value:
            #    return 100, max_conf_correct  # confident the answer is correct
            # else:
            # TODO: might be detected wrong, so check string comparison
            # return 0, max_conf_incorrect / 2
            return check_string(str(answer_value),
                                str(correct_answer_value),
                                min(int(threshold * 1.5), 100),
                                max_conf_incorrect / 2,
                                max_conf_correct / 2)


def check_correct(answer, correct_answer_variants, threshold, max_conf_incorrect, max_conf_correct):
    """
    Check if string answer is correct given correct answer variants and a threshold for correctness
    """
    # TODO: Use question types for the special cases (multiple choice, interval, standard)

    correct = False
    confidence_true = 0
    confidence_false = 100

    for correct_answer_variant in correct_answer_variants:
        # check if given answer is too short
        if len(correct_answer_variant) / len(answer) >= 2:  # Will sometimes be divided by zero
            correct_ratio = 0
            confidence_variant = 100
        else:
            # Compare numbers in the answer
            correct_ratio, confidence_variant = check_numerical_values(answer,
                                                                       correct_answer_variant,
                                                                       threshold,
                                                                       max_conf_incorrect,
                                                                       max_conf_correct)

            if correct_ratio is None:  # No number in correct answer
                # check correctness based on string comparison
                correct_ratio, confidence_variant = check_string(answer,
                                                                 correct_answer_variant,
                                                                 threshold,
                                                                 max_conf_incorrect,
                                                                 max_conf_correct)

        if correct_ratio >= threshold:
            correct = True
            print("Found similar answer in: " + correct_answer_variant)
            if confidence_variant > confidence_true:
                confidence_true = confidence_variant
        else:
            print("Not similar to: " + correct_answer_variant)
            if confidence_variant <= confidence_false:
                confidence_false = confidence_false

    if correct:
        return correct, confidence_true
    else:
        return correct, confidence_false


def check_subanswer_given(subanswer_given, subanswers, threshold, max_conf_incorrect, max_conf_correct):
    print("Read answer: '" + subanswer_given.read_answer + "'")

    correct = False
    confidence_correct = 0
    confidence_false = 100
    most_similar_answer = None  # most similar subanswer

    if len(subanswer_given.read_answer) == 0:  # no answer: incorrect
        return correct, confidence_false
    for subanswer in subanswers:
        variants = [variant.answer for variant in subanswer.variants]  # create usable list for variants
        print("Correct answer variants: " + str(variants))

        correct_temp, confidence_temp = check_correct(subanswer_given.read_answer,
                                                      variants,
                                                      threshold,
                                                      max_conf_incorrect,
                                                      max_conf_correct)

        if correct_temp:
            correct = True
            if confidence_temp >= confidence_correct:
                confidence_correct = confidence_temp
                most_similar_answer = subanswer
        else:  # not correct
            if confidence_temp <= confidence_false:
                confidence_false = confidence_temp

    line_read_confidence_factor = subanswer_given.probability_read_answer ** (1 / float(3))
    if correct:
        confidence = int(confidence_correct * line_read_confidence_factor)
        if most_similar_answer is not None:
            subanswers.remove(most_similar_answer)  # this subanswer can not be used as a correct option anymore
    else:
        confidence = int(confidence_false * line_read_confidence_factor)

    return correct, confidence


def iterate_questions(threshold=50, max_conf_incorrect=50, max_conf_correct=100):
    # TODO: check different thresholds (and their precision & recall) to see which is most reliable
    # TODO: research how confidence ranges based on how "wrong" or "right" answers are
    # TODO: dynamically adjust threshold

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
                # TODO: change threshold based on question type
                if subanswer_given.checkedby.personname == 'nog niet nagekeken':  # == : correct, != : testing
                    correct, confidence = check_subanswer_given(subanswer_given,
                                                                subanswers,
                                                                threshold,
                                                                max_conf_incorrect,
                                                                max_conf_correct)

                    subanswer_given.checkedby = checker
                    subanswer_given.correct = correct
                    subanswer_given.confidence = confidence

                    print("Commiting " + str(correct) + " with confidence " + str(confidence))
                    db.session.commit()
                else:
                    print("Already checked")
                print("")

    print("All questions checked")
