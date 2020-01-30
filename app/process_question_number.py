import pytesseract
import cv2
import numpy as np
import re
from app.save_to_database import save_question_number


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
    save_question_number(question_image, question_number)

    return question_number
