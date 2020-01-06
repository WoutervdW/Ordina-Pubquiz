import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


if __name__ == "__main__":
    print("Hello World")
    img = cv2.imread('naam_new.png')

    text = pytesseract.image_to_string(img)
    print(text)

