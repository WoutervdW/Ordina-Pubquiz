import cv2
import pytesseract
from PIL import Image
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


def show_image(img):
    """
    This will show the image and the program will continue when a key is pressed. Can be used for debugging
    """
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    image_name = "test_11.png"
    img = cv2.imread(image_name)
    show_image(img)
    image_question = cv2.resize(img, (0, 0), fx=5, fy=5)
    show_image(image_question)
    ret, thresh1 = cv2.threshold(image_question, 200, 255, cv2.THRESH_BINARY)
    show_image(thresh1)
    invert = np.invert(img)
    show_image(invert)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 4))
    dilate = cv2.dilate(invert, kernel, iterations=4)
    show_image(dilate)
    invert_thresh = np.invert(thresh1)
    show_image(invert_thresh)

    # print(pytesseract.image_to_string(img, config="--psm 13"))
    # print(pytesseract.image_to_string(image_question, config="--psm 13"))
    # print(pytesseract.image_to_string(thresh1, config="--psm 13"))
    # print(pytesseract.image_to_string(invert, config="--psm 13"))
    # print(pytesseract.image_to_string(dilate, config="--psm 13"))
    # print(pytesseract.image_to_string(invert_thresh, config="--psm 13"))

    print(pytesseract.image_to_string(img, config='outputbase digits'))
    print(pytesseract.image_to_string(image_question, config='outputbase digits'))
    print(pytesseract.image_to_string(thresh1, config='outputbase digits'))
    print(pytesseract.image_to_string(invert, config='outputbase digits'))
    print(pytesseract.image_to_string(dilate, config='outputbase digits'))
    print(pytesseract.image_to_string(invert_thresh, config='outputbase digits'))

    print(pytesseract.image_to_string(img, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789'))
    print(pytesseract.image_to_string(image_question, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789'))
    print(pytesseract.image_to_string(thresh1, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789'))
    print(pytesseract.image_to_string(invert, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789'))
    print(pytesseract.image_to_string(dilate, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789'))
    print(pytesseract.image_to_string(invert_thresh, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789'))


