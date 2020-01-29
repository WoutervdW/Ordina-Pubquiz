from pdf2image import convert_from_path
import numpy as np
import cv2
import os
from PyPDF2 import PdfFileReader

def convert_pdf_to_image(path):
    # First check if the file exists
    print("converting pdf %s" % path)
    if not os.path.isfile(path):
        yield None

    # We check if the path given is a pdf file and not some other file.
    file_extension = os.path.splitext(path)[1]
    if file_extension != ".pdf":
        yield None
    # We also assume the pdf is located 1 folder below but we can just give the name only
    # (I think because we called main.py that will be the working directory)

    # pdf = PdfFileReader(open(path, 'rb'))
    max_pages = 0
    # max_pages = pdf2image._page_count(path)
    with open(path, 'rb') as pdf:
        max_pages = PdfFileReader(pdf).getNumPages()

    print("the amount of pages is %s" % max_pages)
    for page in range(1, max_pages+1, 1):
        print("going to process %s a single page." % path)
        p = convert_from_path(path, dpi=200, first_page=page, last_page=min(page + 1, max_pages))
        print("pdf converted from path")
        print("size of p " + str(len(p)))
        # We are processing it as such that this will always give 1 result. We return the image of the single result
        open_cv_image = np.array(p[0])
        print("pdf turned into an image")
        yield open_cv_image

    # pages = convert_from_path(path, 150)
    #
    # # The image is in PIL format, we will convert it to opencv format
    # open_cv_image = [np.array(p) for p in pages]
    # return open_cv_image

