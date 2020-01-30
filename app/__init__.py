"""
A neural network that reads handwriting from given images.
Based on the project :
'build a handwritten text recognition system'
https://towardsdatascience.com/build-a-handwritten-text-recognition-system-using-tensorflow-2326a3487cd5
"""
import sys
from app.Model import Model
from app.Model import DecoderType
from app.pdf_to_image import convert_pdf_to_image
from app.line_segmentation import line_segmentation, crop_and_warp
from app.word_segmentation import word_segmentation, prepare_image, find_rect, show_image, save_word_image, save_word_details
import os
import cv2
import argparse
from view.models import Answersheet
from view.models import Team
from view.models import SubAnswerGiven
from view.models import SubAnswer
from view.models import Question
from view.models import QuestionNumber
from view.models import Variant
from view.config import InputConfig
import numpy as np
import pytesseract
import re
import app.save_to_database
from fuzzywuzzy import fuzz, process
from view import db


def check_team_name(name_of_team):
    """
    We compare the given team with all the teams that are cooperating in the quiz.
    The team that has the most similarities will be the team that is chosen.
    This is because there can be a mistake with reading the team names
    """
    all_teams = Team.query.all()
    highest_ratio = 0
    team_result = name_of_team
    for t in all_teams:
        t_name = t.get_team_name()
        correct_ratio = fuzz.WRatio(name_of_team, t_name)
        if correct_ratio > highest_ratio:
            highest_ratio = correct_ratio
            team_result = t_name
    # If the team found completely matches a team in the db or if it's the first team it will return what as given.
    return team_result


def read_team(line):
    team_name_image = line
    team_name_image = team_name_image[:, 130:(len(team_name_image[0]))]
    team_name = pytesseract.image_to_string(team_name_image).replace("\n", " ")

    if "Naam:" in team_name:
        print("new team!")
        # We take the name of the team and remove leading whitespaces
        name_of_team = team_name.split("Naam:")[1]
        name_of_team = name_of_team.lstrip()

        name_of_team = check_team_name(name_of_team)

        team_id = save_to_database.save_team_database(name_of_team)
        print("the team name is: " + name_of_team)
        return team_id
    else:
        print("failed!")
        return None


def read_question_number(question_image, previous_question):
    # We remove the right border line from the image to only leave the number
    question_image = question_image[:, 0:(len(question_image[0]) - 10)]

    # Read the number from the number box. After that we remove any non numbers (in case of lines)
    # The configuration is to only read numbers and to look for 1 word
    # TODO @Sander: explain why this pre-processing is done.
    resized_question_number = cv2.resize(question_image, (0, 0), fx=5, fy=5)
    ret, thresh1 = cv2.threshold(resized_question_number, 150, 255, cv2.THRESH_BINARY)
    kernel = np.ones((5, 5), np.uint8)
    erode = cv2.erode(thresh1, kernel, iterations=1)
    blur2 = cv2.blur(erode, (9, 9))

    question_number_resized = pytesseract.image_to_string(resized_question_number,
                                                          config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')
    question_number_blur = pytesseract.image_to_string(blur2,
                                                       config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')

    question_number_resized = re.sub("[^0-9]", "", question_number_resized)
    question_number_blur = re.sub("[^0-9]", "", question_number_blur)

    # The accuracy with the slightly blurred image is the highest
    # The accuracy of the resized is usually enough and it will be used as a fail safe
    question_number = question_number_blur

    # If the number found is the same or 1 higher than previous found number than it is probably correct.
    # We do this to find the improbably inaccuracies with the slightly blurred image.
    if question_number_resized == previous_question or question_number_resized == previous_question + 1:
        question_number = question_number_resized
    if question_number_blur == previous_question or question_number_blur == previous_question + 1:
        question_number = question_number_blur

    # If they both determined the same number we can say with almost absolute certainty that this is the correct number
    if question_number_resized == question_number_blur:
        question_number = question_number_blur

    # save question number to the database (mostly for debugging purposes)
    save_to_database.save_question_number(question_image, question_number)

    return question_number


def process_sheet(answer_sheet_image, model, answersheet_id, sheet_name="scan"):
    sub_answer_number = 0
    previous_question = -1
    team_id = -1
    index = 0
    for line_result in line_segmentation(answer_sheet_image, image_name=sheet_name, answersheet_id=answersheet_id):
        line = line_result[0]
        # The first line of each answersheet will include the team name.
        if index == 0:
            team_id = read_team(line)
            # Each answersheet has a team name, when we read the team name we will update it on the answersheet.
            if not save_to_database.update_team_answersheet(answersheet_id, team_id):
                # We choose to continue and only print a logging for now
                print("there was a problem linking the team to the answersheet")
        index += 1

        # Here we define some parameters of the line used for the processing.
        original_height = line.shape[0]
        resized_height = 50
        multiply_factor = original_height / resized_height
        # After the resizing, the size of the number box will always be around this value.
        number_box_size = 66
        line, question_image = prepare_image(line, resized_height, number_box_size)
        question_number = read_question_number(question_image, previous_question)

        if question_number != "":
            question_id = int(question_number)
            if question_id == previous_question:
                # If this question has the same number as before we should find a variant, because it will have
                # several sub_answers associated with it
                sub_answer_number += 1
            else:
                sub_answer_number = 0
            previous_question = question_id
        else:
            # We turn the question_id to 0. This means it will be ignored.
            question_id = 0

        print("the question number that is read: " + str(question_id))
        res = word_segmentation(line, kernel_size=25, sigma=11, theta=7, min_area=100)
        save_word_details(line_result, multiply_factor, res, number_box_size, db, model, team_id, question_id, sub_answer_number)


def process_sheet_old(answer_sheet_image, model, save_image=False, sheet_name="scan", db=None, answersheet_id=None):

    # We keep track of which question is being handled, because 1 question can have multiple lines
    sub_answer_number = 0
    previous_question = -1

    # Now we have the answer sheet in image form and we can move on to the line segmentation
    output_folder = "out/"
    lines = line_segmentation(answer_sheet_image, save_image, output_folder, sheet_name, db, answersheet_id)

    # The first line of the answersheet can be the team name. We will check if this is indeed the name
    # We choose 130 as the bound for the left box length
    team_name_image = lines[0][0]
    team_name_image = team_name_image[:, 130:(len(team_name_image[0]))]
    team_name = pytesseract.image_to_string(team_name_image).replace("\n", " ")

    team_id = -1
    if "Naam:" in team_name:
        print("new team!")
        # We take the name of the team and remove leading whitespaces
        name_of_team = team_name.split("Naam:")[1]
        name_of_team = name_of_team.lstrip()

        name_of_team = check_team_name(name_of_team)

        team_id = save_to_database.save_team_database(name_of_team)
        print("the team name is: " + name_of_team)
    else:
        print("failed!")

    # If no team name is found it should use it's previously found team_id
    if not save_to_database.update_team_answersheet(answersheet_id, team_id):
        # We choose to continue and only print a logging for now
        print("there was a problem linking the team to the answersheet")

    for line_image in lines:
        line = line_image[0]
        # -kernelSize: size of filter kernel (odd integer)
        # -sigma: standard deviation of Gaussian function used for filter kernel
        # -theta: approximated width/height ratio of words, filter function is distorted by this factor
        # - min_area: ignore word candidates smaller than specified area
        original_height = line.shape[0]
        resized_height = 50
        multiply_factor = original_height / resized_height
        # After the resizing, the size of the number box will always be around this value.
        number_box_size = 66
        line, question_image = prepare_image(line, resized_height, number_box_size)
        # TODO test out the theta and min_area parameter changes if the results are not good.
        res = word_segmentation(line, kernel_size=25, sigma=11, theta=7, min_area=100)

        # We remove the right border line from the image to only leave the number
        question_image = question_image[:, 0:(len(question_image[0]) - 10)]

        # Read the number from the number box. After that we remove any non numbers (in case of lines)
        # The configuration is to only read numbers and to look for 1 word
        # TODO @Sander: explain why this pre-processing is done.
        resized_question_number = cv2.resize(question_image, (0, 0), fx=5, fy=5)
        ret, thresh1 = cv2.threshold(resized_question_number, 150, 255, cv2.THRESH_BINARY)
        kernel = np.ones((5, 5), np.uint8)
        erode = cv2.erode(thresh1, kernel, iterations=1)
        blur2 = cv2.blur(erode, (9, 9))

        question_number_resized = pytesseract.image_to_string(resized_question_number,
                                                      config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')
        question_number_blur = pytesseract.image_to_string(blur2,
                                                           config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')

        question_number_resized = re.sub("[^0-9]", "", question_number_resized)
        question_number_blur = re.sub("[^0-9]", "", question_number_blur)

        # The accuracy with the slightly blurred image is the highest
        # The accuracy of the resized is usually enough and it will be used as a fail safe
        question_number = question_number_blur

        # If the number found is the same or 1 higher than previous found number than it is probably correct.
        # We do this to find the improbably innaccuracies with the slightly blurred image.
        if question_number_resized == previous_question or question_number_resized == previous_question + 1:
            question_number = question_number_resized
        if question_number_blur == previous_question or question_number_blur == previous_question + 1:
            question_number = question_number_blur

        # If they both determined the same number we can say with almost certainty that this is the correct number
        if question_number_resized == question_number_blur:
            question_number = question_number_blur

        q_image = question_image.tostring()

        question_width = len(question_image)
        question_height = len(question_image[0])
        if db is not None:
            # TODO fill in the other details as well! (not just the image)
            question_recognized = QuestionNumber(
                question_number=question_number,
                question_image=q_image,
                image_width=question_width,
                image_height=question_height
            )
            # add the object to the database session
            db.session.add(question_recognized)
            # commit the session so that the image is stored in the database
            db.session.commit()

        if question_number != "":
            question_id = int(question_number)
            if question_id == previous_question:
                # If this question has the same number as before we should find a variant, because it will have
                # several subanswers associated with it
                sub_answer_number += 1
            else:
                sub_answer_number = 0
            previous_question = question_id
        else:
            # We turn the question_id to 0. This means it will be ignored.
            question_id = 0

        print("the question number that is read: " + str(question_id))
        save_word_details(line_image, multiply_factor, res, number_box_size, db, model, team_id, question_id, sub_answer_number)


def run_pubquiz_program(answer_sheets):
    print("De officiele Ordina pub-quiz antwoord vinder")
    model = Model(open('model/charList.txt').read())

    index = 0
    for p in convert_pdf_to_image(answer_sheets):
        if p is not None:
            file_extension = os.path.splitext(answer_sheets)
            sheet_name = answer_sheets
            if file_extension[1] == ".pdf":
                sheet_name = sheet_name[0:-4]
            sheet_name = sheet_name + "_" + str(index)
            index += 1

            answersheet_id = save_to_database.save_answersheet_database(p)

            if answersheet_id == -1:
                return "Er is iets fout gegaan. Probeer opnieuw."
            else:
                process_sheet(p, model, answersheet_id, sheet_name=sheet_name)
        else:
            return "Bestand uploaden mislukt. Het bestand kan niet uitgelezen worden."


def save_answersheet():
    pubquiz_anser_sheets = 'scan.pdf'
    pages = convert_pdf_to_image(pubquiz_anser_sheets)
    return pages

