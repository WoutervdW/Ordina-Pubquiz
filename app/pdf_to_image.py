from pdf2image import convert_from_path
import numpy as np
import cv2
import os


def convert_pdf_to_image(path):
    # First check if the file exists
    if not os.path.isfile(path):
        return None

    # We check if the path given is a pdf file and not some other file.
    file_extension = os.path.splitext(path)[1]
    if file_extension != ".pdf":
        return None
    # We also assume the pdf is located 1 folder below but we can just give the name only
    # (I think because we called main.py that will be the working directory)
    pages = convert_from_path(path, 150)

    # The image is in PIL format, we will convert it to opencv format
    open_cv_image = [np.array(p) for p in pages]
    return open_cv_image

