import pytesseract
import cv2
import numpy as np
import re
from app.save_to_database import save_question_number


def read_question_number(question_image, previous_question):
    # We remove the right border line from the image to only leave the number
    question_image = question_image[:, 0:(len(question_image[0]) - 10)]
    average_image = []
    for line in question_image:
        average_image.append(np.average(line))

    result = np.average(average_image)
    # If the image is completely blank, than the average over all the pixel values will be close to 255. We take all
    # the results below the 253 values because the darkness of the letters insures that the average value will be below
    # this threshold. This is an easy and effective filter technique to only read the lines that matter
    if result < 253:
        # Read the number from the number box. After that we remove any non numbers (in case of lines)
        # The configuration is to only read numbers and to look for 1 word
        # TODO @Sander: explain why this pre-processing is done.
        resized_question_number = cv2.resize(question_image, (0, 0), fx=3, fy=3)
        ret, thresh1 = cv2.threshold(resized_question_number, 200, 255, cv2.THRESH_BINARY)
        kernel = np.ones((4, 4), np.uint8)
        erode = cv2.dilate(thresh1, kernel, iterations=1)
        blur2 = cv2.blur(erode, (4, 4))

        question_number_blur = pytesseract.image_to_string(blur2,
                                                           config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')

        read_number_blur = re.sub("[^0-9]", "", question_number_blur)
        question_number = read_number_blur

        # save question number to the database (mostly for debugging purposes) turned off in real settings for speed
        save_question_number(blur2, question_number)
        return question_number
    else:
        return 0
