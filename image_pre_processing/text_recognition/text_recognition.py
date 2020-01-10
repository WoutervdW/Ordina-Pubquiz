import cv2
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


def show_image(img):
    """
    This will show the image and the program will continue when a key is pressed. Can be used for debugging
    """
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    image_name = "question_number_6.png"
    img = cv2.imread(image_name)
    show_image(img)
    image_question = cv2.resize(img, (0, 0), fx=5, fy=5)
    show_image(image_question)
    ret, thresh1 = cv2.threshold(image_question, 200, 255, cv2.THRESH_BINARY)
    show_image(thresh1)

    # print(pytesseract.image_to_string(img))
    print(pytesseract.image_to_string(img, config="--psm 13"))

