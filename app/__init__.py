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

line_number = 0


def process_sheet(answer_sheet_image, model, save_image=False, sheet_name="scan", db=None, team_id=None, answersheet_id=None):
    global line_number
    # gray = cv2.cvtColor(answer_sheet_image, cv2.COLOR_BGR2GRAY)
    # Now we have the answer sheet in image form and we can move on to the line segmentation
    output_folder = "out/"
    lines = line_segmentation(answer_sheet_image, save_image, output_folder, sheet_name, db, answersheet_id)

    # We keep track of which question is being handled, because 1 question can have multiple lines
    prev_question = -1
    subanswer_number = 0
    question_id = 0
    # The first line of the answersheet can be the team name. We will check if this is indeed the name
    # We choose 130 as the bound for the left box length
    team_name_image = lines[0][0]
    team_name_image = team_name_image[:, 130:(len(team_name_image[0]))]
    team_name = pytesseract.image_to_string(team_name_image).replace("\n", " ")
    if "NAAM:" in team_name:
        print("new team!")
        # We take the name of the team and remove leading whitespaces
        name_of_team = team_name.split("NAAM:")[1]
        name_of_team = name_of_team.lstrip()
        team_id = save_to_database.save_team_database(db, name_of_team)
        print("the team name is: " + name_of_team)
        print("the team id is: " + str(team_id))

    save_to_database.update_team_answersheet(db, answersheet_id, team_id)

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
        question_number = pytesseract.image_to_string(question_image, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')
        question_number = re.sub("[^0-9]", "", question_number)

        q_image = question_image.tostring()

        question_width = len(question_image)
        question_height = len(question_image[0])
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

        # line_detail = InputConfig.quiz[line_number]
        if question_number != "":
            question_id = int(question_number)
            # If the line detail is a number, this corresponds to the question
            print("processing question: " + str(question_id))
            if question_id == prev_question:
                subanswer_number += 1
            else:
                prev_question = question_id
                subanswer_number = 0

        print("the question number that is read: " + str(question_id) + " the number of the question: " + str(InputConfig.quiz[line_number]))
        save_word_details(line_image, multiply_factor, res, number_box_size, db, model, answersheet_id, line_number, question_id, subanswer_number)


def run_program(pubquiz_answer_sheets, save_image=False, db=None):
    print("De officiele Ordina pub-quiz antwoord vinder")
    model = Model(open('model/charList.txt').read())

    answersheet_id = -1
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
                process_sheet(pages[p], model, save_image, sheet_name, db, team_id, answersheet_id)

    global line_number
    line_number = 0


def save_answersheet():
    pubquiz_anser_sheets = 'scan.pdf'
    pages = convert_pdf_to_image(pubquiz_anser_sheets)
    return pages

