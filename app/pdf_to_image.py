from pdf2image import convert_from_path
import numpy as np
import cv2


def convert_pdf_to_image(path):
    # We also assume the pdf is located 1 folder below but we can just give the name only
    # (I think because we called main.py that will be the working directory)
    pages = convert_from_path(path, 500)

    # We assume there is only 1 scanned image at the time.
    # The image is in PIL format, we will convert it to opencv format
    # open_cv_image = np.array(pages[0])
    # return open_cv_image
    return cv2.cvtColor(np.array(pages[0]), cv2.COLOR_RGB2BGR)

