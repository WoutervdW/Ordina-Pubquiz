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
from view.models import Variant
from view.config import InputConfig
import numpy as np

line_number = 0


def process_sheet(answer_sheet_image, model, save_image=False, sheet_name="scan", db=None, answersheet_id=None):
    global line_number
    # gray = cv2.cvtColor(answer_sheet_image, cv2.COLOR_BGR2GRAY)
    # Now we have the answer sheet in image form and we can move on to the line segmentation
    output_folder = "out/"
    lines = line_segmentation(answer_sheet_image, save_image, output_folder, sheet_name, db, answersheet_id)

    # We keep track of which question is being handled, because 1 question can have multiple lines
    prev_question = -1
    subanswer_number = 0
    # After the line segmentation is done we can find the separate words
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
        line = prepare_image(line, resized_height, number_box_size)
        # TODO test out the theta and min_area parameter changes if the results are not good.
        res = word_segmentation(line, kernel_size=25, sigma=11, theta=7, min_area=100)

        # iterate over all segmented words
        # print('Segmented into %d words' % len(res))
        # if save_image:
        #     save_word_image(output_folder, sheet_name, line_image, multiply_factor, res, number_box_size)
        # #
        # We can now examine each word.
        answersheet_detail = InputConfig.page_lines[1]
        line_detail = answersheet_detail[line_number]
        question_id = InputConfig.question_to_id.get(str(line_detail))
        if question_id == prev_question:
            subanswer_number += 1
        else:
            prev_question = question_id
            subanswer_number = 0
        save_word_details(line_image, multiply_factor, res, number_box_size, db, model, answersheet_id, line_number, subanswer_number)


def run_program(pubquiz_answer_sheets, save_image=False, db=None):
    print("De officiele Ordina pub-quiz antwoord vinder")
    model = Model(open('model/charList.txt').read())

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

            answersheet_id = 0
            if db is not None:
                print("linking team to page")
                # We will link the answersheet to the correct team. If it does not exist we will create it.
                team = Team.query.filter_by(teamname=InputConfig.team_page[p]).first()
                if team is None:
                    # The team does not exist yet, so we will create it with 0 score.
                    new_team = Team(
                        teamname=InputConfig.team_page[p],
                        score=0
                    )
                    db.session.add(new_team)
                    # We already commit it because we need to query it right after to find the id.
                    db.session.commit()

                print("saving answersheet to the database")
                # Save the image to the database!
                # convert the image to byte array so it can be saved in the database
                answer = pages[p].tostring()
                # create an Image object to store it in the database
                width = len(pages[p])
                height = len(pages[p][0])

                # We know a team exists with the configured name because if it didn't we just created it.
                team = Team.query.filter_by(teamname=InputConfig.team_page[p]).first()
                new_answersheet = Answersheet(
                    answersheet_image=answer,
                    team_id=team.id,
                    image_width=width,
                    image_height=height
                )
                # add the object to the database session
                db.session.add(new_answersheet)
                # commit the session so that the image is stored in the database
                db.session.commit()
                answersheet_id = new_answersheet.id

            process_sheet(pages[p], model, save_image, sheet_name, db, answersheet_id)


def save_answersheet():
    pubquiz_anser_sheets = 'scan.pdf'
    pages = convert_pdf_to_image(pubquiz_anser_sheets)
    return pages

