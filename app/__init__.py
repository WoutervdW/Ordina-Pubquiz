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

line_number = 0
team_id = -1


def check_team_name(name_of_team):
    """
    We compare the given team with all the teams that are cooperating in the quiz.
    The team that has the most simolarities will be the team that is chosen.
    This is because there can be a mistake with reading the team names
    """

    all_teams = Team.query.all()
    higest_ration = 0
    team_result = name_of_team
    for t in all_teams:
        t_name = t.get_team_name()
        correct_ratio = fuzz.WRatio(name_of_team, t_name)
        if correct_ratio > higest_ration:
            higest_ration = correct_ratio
            team_result = t_name
    return team_result


def process_sheet(answer_sheet_image, model, save_image=False, sheet_name="scan", db=None, answersheet_id=None):
    global line_number
    global team_id

    # We keep track of which question is being handled, because 1 question can have multiple lines
    prev_question = -1
    subanswer_number = 0
    question_id = 0
    previous_question = -1

    # Now we have the answer sheet in image form and we can move on to the line segmentation
    output_folder = "out/"
    lines = line_segmentation(answer_sheet_image, save_image, output_folder, sheet_name, db, answersheet_id)

    # The first line of the answersheet can be the team name. We will check if this is indeed the name
    # We choose 130 as the bound for the left box length
    team_name_image = lines[0][0]
    team_name_image = team_name_image[:, 130:(len(team_name_image[0]))]
    team_name = pytesseract.image_to_string(team_name_image).replace("\n", " ")
    if "Naam:" in team_name:
        print("new team!")
        # We take the name of the team and remove leading whitespaces
        name_of_team = team_name.split("Naam:")[1]
        name_of_team = name_of_team.lstrip()

        name_of_team = check_team_name(name_of_team)

        team_id = save_to_database.save_team_database(db, name_of_team)
        # Now that we have a new team, we will also reset the line number counter
        line_number = 0
        print("the team name is: " + name_of_team)
        print("the team id is: " + str(team_id))

    # If no team name is found it should use it's previously found team_id
    if not save_to_database.update_team_answersheet(db, answersheet_id, team_id):
        # We choose to continue and only print a logging for now
        print("there was a problem linking the team to the answersheet")

    for line_image in lines:
        line_number += 1
        print("processing line: " + str(line_number))
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
        ret, thresh1 = cv2.threshold(resized_question_number, 180, 255, cv2.THRESH_BINARY)
        blur2 = cv2.blur(thresh1, (10, 10))
        question_number = pytesseract.image_to_string(blur2, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')
        question_number = re.sub("[^0-9]", "", question_number)

        q_image = blur2.tostring()

        question_width = len(blur2)
        question_height = len(blur2[0])
        if db is not None:
            print("save question number to database with width %s and height %s" % (question_width, question_height))
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
                subanswer_number += 1
            else:
                subanswer_number = 0
            previous_question = question_id
        else:
            # If the question number was empty this should be ignored.
            print("ignore this line")
            # We turn the question_id to 0. This means it will be ignored.
            question_id = 0

        print("the question number that is read: " + str(question_id))
        save_word_details(line_image, multiply_factor, res, number_box_size, db, model, team_id, question_id, subanswer_number)


def run_program(pubquiz_answer_sheets, save_image=False, db=None):
    print("De officiele Ordina pub-quiz antwoord vinder")
    model = Model(open('model/charList.txt').read())

    answersheet_id = -1
    global team_id
    team_id = -1
    for answer_sheets in pubquiz_answer_sheets:
        # The pdf file. We can it and it returns 1 to multiple answer pages
        pages = convert_pdf_to_image(answer_sheets)
        for p in range(0, len(pages)):
            # We take the name from the file. But we want it without any extension.
            file_extension = os.path.splitext(answer_sheets)
            sheet_name = answer_sheets
            if file_extension[1] == ".pdf":
                sheet_name = sheet_name[0:-4]
            sheet_name = sheet_name + "_" + str(p)

            answersheet_id = save_to_database.save_answersheet_database(db, pages[p])

            if answersheet_id == -1:
                print("something went wrong, no answersheet id present")
                exit()
            else:
                print("start processing answersheet with id " + str(answersheet_id))
                process_sheet(pages[p], model, save_image, sheet_name, db, answersheet_id)

    global line_number
    line_number = 0


def save_answersheet():
    pubquiz_anser_sheets = 'scan.pdf'
    pages = convert_pdf_to_image(pubquiz_anser_sheets)
    return pages

