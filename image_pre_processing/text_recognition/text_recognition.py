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
    image_name = "test_48.png"
    img = cv2.imread(image_name)
    show_image(img)
    image_question = cv2.resize(img, (0, 0), fx=5, fy=5)
    show_image(image_question)
    ret, thresh1 = cv2.threshold(image_question, 125, 255, cv2.THRESH_BINARY)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 4))

    show_image(thresh1)
    invert = np.invert(image_question)
    show_image(invert)
    dilate = cv2.dilate(invert, kernel, iterations=3)
    show_image(dilate)

    resize_2 = cv2.resize(img, None, fx=5, fy=5, interpolation=cv2.INTER_CUBIC)
    show_image(resize_2)
    blur1 = cv2.blur(resize_2, (10, 10))
    show_image(blur1)
    blur2 = cv2.GaussianBlur(resize_2, (9, 9), 0)
    show_image(blur2)
    blur3 = cv2.medianBlur(resize_2, 5)
    show_image(blur3)

    # print(pytesseract.image_to_string(img, config="--psm 13"))
    # print(pytesseract.image_to_string(image_question, config="--psm 13"))
    # print(pytesseract.image_to_string(thresh1, config="--psm 13"))
    # print(pytesseract.image_to_string(invert, config="--psm 13"))
    # print(pytesseract.image_to_string(dilate, config="--psm 13"))
    # print(pytesseract.image_to_string(invert_thresh, config="--psm 13"))
    #
    # print(pytesseract.image_to_string(img, config='outputbase digits'))
    # print(pytesseract.image_to_string(image_question, config='outputbase digits'))
    # print(pytesseract.image_to_string(thresh1, config='outputbase digits'))
    # print(pytesseract.image_to_string(invert, config='outputbase digits'))
    # print(pytesseract.image_to_string(dilate, config='outputbase digits'))
    # print(pytesseract.image_to_string(invert_thresh, config='outputbase digits'))
    #
    print(pytesseract.image_to_string(img, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789'))
    print(pytesseract.image_to_string(image_question, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789'))
    print(pytesseract.image_to_string(thresh1, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789'))
    print(pytesseract.image_to_string(invert, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789'))
    print(pytesseract.image_to_string(dilate, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789'))
    print("new tests")
    print(pytesseract.image_to_string(resize_2, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789'))
    print(pytesseract.image_to_string(blur1, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789'))
    print(pytesseract.image_to_string(blur2, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789'))
    print(pytesseract.image_to_string(blur3, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789'))

    # result = pytesseract.image_to_string(team_name_image)
    # print(result.replace("\n", " "))
    # print(pytesseract.image_to_string(image_question))
    # print(pytesseract.image_to_string(thresh1))
    # print(pytesseract.image_to_string(invert))
    # print(pytesseract.image_to_string(dilate))
    # print(pytesseract.image_to_string(invert_thresh))


