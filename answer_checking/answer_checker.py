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
    # all_word_chars_pattern = re.compile(r'\w+')  # remove all but numbers and letters
    # answer = all_word_chars_pattern.findall(answer)  # get all individual letters and numbers sequences
    # answer = ''.join(map(str, answer))
    return answer


def check_string(answer, correct_answer_variant):
    # TODO: use several different string comparison techniques to get better results and confidence

    # pre-process strings
    answer = preprocess_string(answer)
    correct_answer_variant = preprocess_string(correct_answer_variant)

    # calculate correct ratio
    correct_ratio = fuzz.ratio(answer, correct_answer_variant)
    return correct_ratio


def check_numerical_value2(answer_value, correct_answer_value):
    if answer_value == correct_answer_value:
        return 100
    else:
        return 0


def remove_special_chars(answer, correct_answer_variant):
    # Remove all non-alphabetic and non-numerical symbols from the given answer, if the correct answer doesn't contain
    # them
    all_non_word_pattern = re.compile(r'([^\s\w])+')  # match anything that isn't a whitespace or word character
    non_word_chars_in_correct_answer = all_non_word_pattern.findall(correct_answer_variant)
    non_word_chars_in_answer = all_non_word_pattern.findall(answer)
    if len(non_word_chars_in_correct_answer) == 0 and len(non_word_chars_in_answer) != 0:
        all_words_pattern = re.compile(r'[\s\w]+')  # match only whitespace or word characters
        words_in_answer = all_words_pattern.findall(answer)
        answer = ''.join(map(str, words_in_answer))
    answer = answer.strip()
    return answer


def get_correct_ratio_numbers(answer, correct_answer_variant):
    # TODO: possibly compare each number sequence in the correct answer to each number sequence in the given answer
    all_digits_pattern = re.compile(r'\d+')  # get all individual numbers. NO SPACES FOR NOW

    # Find all numbers
    answer_values = all_digits_pattern.findall(answer)  # Find all numbers in the answer
    correct_answer_values = all_digits_pattern.findall(correct_answer_variant)  # Find all numbers in the correct answer

    if len(answer_values) == 0 or len(correct_answer_values) == 0:
        return 0

    # join the number parts and compare them. correct_ratio * ratio of the word that is numbers
    answer_val = int(''.join(map(str, answer_values)))
    correct_answer_value = int(''.join(map(str, correct_answer_values)))
    correct_ratio_numbers = check_numerical_value2(answer_val, correct_answer_value)
    correct_ratio_numbers = correct_ratio_numbers * (len(str(correct_answer_value)) / len(str(correct_answer_variant)))
    return correct_ratio_numbers


def get_correct_ratio_string(answer, correct_answer_variant):
    all_non_digits_pattern = re.compile(r'\D+')  # get all non-numbers

    # Find all non-numbers
    answer_components = all_non_digits_pattern.findall(answer)
    correct_answer_components = all_non_digits_pattern.findall(correct_answer_variant)

    # join the string parts and compare them. correct_ratio * ratio of the word that is string
    answer_str = ''.join(map(str, answer_components))
    correct_answer_str = ''.join(map(str, correct_answer_components))
    correct_ratio_str = check_string(answer_str, correct_answer_str)
    correct_ratio_str = correct_ratio_str * (len(correct_answer_str) / len(correct_answer_variant))
    return correct_ratio_str


def check_correct(answer, correct_answer_variants, threshold, max_conf_incorrect, max_conf_correct):
    """
    Check if string answer is correct given correct answer variants and a threshold for correctness
    """
    # TODO: Use question types for the special cases (multiple choice, interval, standard)

    correct = False
    confidence_true = 0
    confidence_false = 100

    for correct_answer_variant in correct_answer_variants:
        answer = remove_special_chars(answer, correct_answer_variant)
        correct_answer_variant = correct_answer_variant.strip()
        # check if answer has only random characters (krasdetectie) or is too short
        if len(answer) == 0 or len(correct_answer_variant) / len(answer) > 2:
            correct_ratio = 0
            confidence_variant = 100
        else:
            correct_ratio_numbers = get_correct_ratio_numbers(answer, correct_answer_variant)
            print(correct_ratio_numbers)
            correct_ratio_str = get_correct_ratio_string(answer, correct_answer_variant)
            print(correct_ratio_str)

            # add up the correct_ratios.
            correct_ratio = correct_ratio_str + correct_ratio_numbers
            print("Correct ratio: " + str(correct_ratio))

            # calculate the confidence
            confidence_variant = calculate_confidence(correct_ratio, threshold, max_conf_incorrect, max_conf_correct)
            print("confidence: " + str(confidence_variant))

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
                most_similar_answer = subanswer  # remember most similar answer
        else:  # not correct
            if confidence_temp <= confidence_false:  # if the answer is wrong, but not completely, save this uncertainty
                confidence_false = confidence_temp
    print(subanswer_given.probability_read_answer)
    line_read_confidence_factor = subanswer_given.probability_read_answer ** (1 / float(3))
    print(line_read_confidence_factor)
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
                if subanswer_given.checkedby.personname != 'nog niet nagekeken':  # == : correct, != : testing
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
