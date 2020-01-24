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
    image_name = "test_9.png"
    img = cv2.imread(image_name)
    # show_image(img)
    resized_question_number = cv2.resize(img, (0, 0), fx=5, fy=5)
    show_image(resized_question_number)
    ret, thresh1 = cv2.threshold(resized_question_number, 150, 255, cv2.THRESH_BINARY)
    show_image(thresh1)
    kernel = np.ones((5, 5), np.uint8)
    erode = cv2.erode(thresh1, kernel, iterations=1)
    show_image(erode)
    blur2 = cv2.blur(erode, (9, 9))
    show_image(blur2)
    print(pytesseract.image_to_string(blur2, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789'))

    resized_question_number = cv2.resize(img, (0, 0), fx=7, fy=7)
    # show_image(resized_question_number)
    ret, thresh1 = cv2.threshold(resized_question_number, 210, 255, cv2.THRESH_BINARY)
    # show_image(thresh1)
    blur2 = cv2.blur(thresh1, (8, 8))
    blurg = cv2.GaussianBlur(thresh1, (15, 15), cv2.BORDER_DEFAULT)
    show_image(blur2)
    show_image(blurg)
    print(pytesseract.image_to_string(blurg, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789'))

    resized_question_number = cv2.resize(img, (0, 0), fx=12, fy=12)
    # show_image(resized_question_number)
    ret, thresh1 = cv2.threshold(resized_question_number, 210, 255, cv2.THRESH_BINARY)
    # show_image(thresh1)
    blur2 = cv2.blur(thresh1, (15, 15))
    print(pytesseract.image_to_string(blur2, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789'))
