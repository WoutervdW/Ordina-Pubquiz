from fuzzywuzzy import fuzz, process
import re
from view.models import Team
from view.models import SubAnswerGiven
from view.models import SubAnswer
from view.models import Variant, Person
from view import db


# TODO: check string similarity using fuzzywuzzy (https://www.datacamp.com/community/tutorials/fuzzy-string-python)
# TODO: Remove the entry from the list if it has been checked, to prevent duplicate answers from scoring points.
# TODO: compare numbers as ints
# TODO: get the Question from calculate_score to string comparison for the category to parse the string correctly
#  (numbers in songs should be parsed as strings, in other answers they should probably be parsed as integers)

# TODO: get questions from database


def check_correct(answer, correct_answer_variants):
    """

    :param answer: string of given answer
    :param correct_answer_variants: list of strings: variants of correct answer
    :return:
    """
    # number_correct has to be True if the number exists and is correct, False if the number exists but isn't
    # correct and None if no number exists
    for correct_answer_variant in correct_answer_variants:
        number_correct = check_numerical_values(answer, correct_answer_variant)  # Compare numbers in the answer
        if number_correct is None:
            # No number in given answer, check correctness based on string-based comparison
            return check_string(answer, correct_answer_variant)
        elif number_correct:
            # Number correct, see if the rest of the string is also correct.
            # TODO: Combine the correctness of the string and number parts
            return True
    return False


def check_numerical_values(answer, correct_answer_variant):
    """
    Find all numbers in the answer
    :param answer: string
    :param correct_answer_variant: string
    :return: None if no number in given answer, True if correct number in given answer, False if incorrect number
    """
    all_digits_pattern = re.compile(r'\d+')  # get all individual numbers
    answer_values = all_digits_pattern.findall(answer)  # Find all numbers in the answer
    correct_answer_values = all_digits_pattern.findall(correct_answer_variant)  # Find all numbers in the correct answer

    if len(answer_values) == 0:
        # no number in given answer
        return None
    elif len(answer_values) != 0 and len(correct_answer_values) != 0:
        answer_value = int(''.join(map(str, answer_values)))  # concatenate all numbers in the answer
        correct_answer_value = int(''.join(map(str, correct_answer_values)))  # concatenate all numbers in the answer
        if answer_value == correct_answer_value:
            return True
    else:
        return False


def check_string(answer, correct_answer_variant):
    answer = preprocess_string(answer)
    correct_answer_variant = preprocess_string(correct_answer_variant)

    # Select the string with the highest matching percentage
    # highest = process.extractOne(answer, correct_answers)
    # correct_answer_list.remove(highest[0])
    # TODO @Wouter: return the ratio of correctness ("confidence") AND the decision of correctness
    #  Implement confidence as distance of correctness from 0 or 100 (the closer to 50%, the less confident we can
    #  be that the answer is actually wrong or right)
    return fuzz.WRatio(answer, correct_answer_variant) > 80


def preprocess_string(answer):
    answer = answer.lower()
    return answer


def check_all_answers():
    print("Checking all answers")
    # get all given subanswers
    all_subanswers_given = SubAnswerGiven.query.all()
    checker = Person.query.filter_by(personname="systeem").first()

    # check correctness per given answer
    for subanswer_given in all_subanswers_given:
        print("Given answer: " + subanswer_given.answer_given)

        # Get the question id of the given answer
        question_id = subanswer_given.question_id

        # Get the list of all subanswers that belong to the same question as subanswer_given
        subanswers = SubAnswer.query.filter_by(question_id=question_id).all()

        # Get all variants for each subanswer and append them into one (python) list
        variant_lists = []
        for subanswer in subanswers:
            subanswer_id = subanswer.id
            variants = Variant.query.filter_by(subanswer_id=subanswer_id)
            variants = [variant.answer for variant in variants]
            variant_lists.append(variants)

        print("Correct answer options: " + str(variant_lists))

        # check all
        for variants in variant_lists:
            # TODO @wouter: remember checked answers! If an answer occurs twice, the second instance should not be
            #  correct (If the same answer twice is correct, than the "correct answers" should contain two of the
            #  same answer). So, the first instance should be removed.
            if check_correct(subanswer_given.answer_given, variants):
                print("correct")
                subanswer_given.correct = True
                variant_lists.remove(variants)
                break
            else:
                print("incorrect")
                subanswer_given.correct = False
                # variant_lists.remove(variants)
            subanswer_given.checkedby = checker
            db.session.commit()
            # TODO @wouter: change correct / incorrect buttons automatically live in view
