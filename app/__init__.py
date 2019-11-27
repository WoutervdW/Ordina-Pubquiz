"""
A neural network that reads handwriting from given images.
Based on the project :
'build a handwritten text recognition system'
https://towardsdatascience.com/build-a-handwritten-text-recognition-system-using-tensorflow-2326a3487cd5
"""
import sys
from app.Model import Model
from app.Model import DecoderType
from app.SamplePreprocessor import preprocess
from app.DataLoader import Batch
from app.pdf_to_image import convert_pdf_to_image
from app.line_segmentation import line_segmentation, crop_and_warp
from app.word_segmentation import word_segmentation, prepare_image, find_rect, show_image, save_word_image
import os
import cv2
import argparse


def infer(_model, fn_img):
    """
    recognize text in image provided by file path
    """
    image = preprocess(cv2.imread(fn_img, cv2.IMREAD_GRAYSCALE), Model.img_size)
    batch = Batch([image])
    (recognized, probability) = _model.infer_batch(batch, True)
    print('Recognized:', '"' + recognized[0] + '"')
    print('Probability:', probability[0])


def read_word_from_image(image_to_read):
    model = Model(open('model/charList.txt').read())
    image_to_read = ['test-images/handgeschreven_thick.png']
    # A simple example of how we could possibly use arguments to determine what image is tested
    # TODO make it better.
    # for eachArg in sys.argv:
    #     image_to_read.append(eachArg)

    for image in image_to_read:
        infer(model, image)

    # # After the model is loaded we can very quickly load another image.
    # image_to_read_2 = 'test-images/tekst_thick.png'
    # infer(model, image_to_read_2)


def process_sheet(answer_sheet_image, save_image=False, sheet_name="scan"):
    # gray = cv2.cvtColor(answer_sheet_image, cv2.COLOR_BGR2GRAY)
    # Now we have the answer sheet in image form and we can move on to the line segmentation
    output_folder = "out/"
    lines = line_segmentation(answer_sheet_image, save_image, output_folder, sheet_name)

    index = 0
    # After the line segmentation is done we can find the separate words
    for line_image in lines:
        line = line_image[0]
        # -kernelSize: size of filter kernel (odd integer)
        # -sigma: standard deviation of Gaussian function used for filter kernel
        # -theta: approximated width/height ratio of words, filter function is distorted by this factor
        # - min_area: ignore word candidates smaller than specified area
        original_height = line.shape[0]
        resized_height = 50
        multiply_factor = original_height / resized_height
        line = prepare_image(line, resized_height)
        # TODO test out the theta and min_area parameter changes if the results are not good.
        res = word_segmentation(line, kernel_size=25, sigma=11, theta=5, min_area=150)

        # iterate over all segmented words
        print('Segmented into %d words' % len(res))
        if save_image:
            save_word_image(output_folder, sheet_name, line_image, multiply_factor, res)


def run(pubquiz_answer_sheets, save_image=False):
    print("De officiele Ordina pub-quiz antwoord vinder")

    for answer_sheets in pubquiz_answer_sheets:
        # The pdf file. We can it and it returns 1 to multiple answer pages
        pages = convert_pdf_to_image(answer_sheets)
        for p in range(0, len(pages)):
            # We take the name from the file. But we want it without any extension.
            file_extension = os.path.splitext(answer_sheets)
            sheet_name = answer_sheets
            if file_extension[1] == ".pdf":
                sheet_name = sheet_name[0:-4]
            sheet_name = sheet_name + "_" + str(p)
            process_sheet(pages[p], save_image, sheet_name)

