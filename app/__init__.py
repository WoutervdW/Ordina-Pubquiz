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
from app.word_segmentation import word_segmentation, prepare_image, find_rect, show_image, save_word_image, get_words_image
import os
import cv2
import argparse


def infer(_model, word_image):
    """
    recognize text in image provided by file path
    """
    # image = fn_img
    fn_img = cv2.cvtColor(word_image, cv2.COLOR_BGR2GRAY)
    image = preprocess(fn_img, Model.img_size)
    batch = Batch([image])
    (recognized, probability) = _model.infer_batch(batch, True)
    print('Recognized:', '"' + recognized[0] + '"')
    print('Probability:', probability[0])
    return recognized, probability


def read_word_from_image(image_to_read, model):
    results = infer(model, image_to_read)
    return results


def process_sheet(answer_sheet_image, model, save_image=False, sheet_name="scan"):
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

        # We can now examine each word.
        words = get_words_image(line_image, multiply_factor, res)
        words_results = []
        for word in words:
            # TODO add contrast to each word
            read_results = read_word_from_image(word, model)
            words_results.append(read_results)
            print(words_results)



def run(pubquiz_answer_sheets, save_image=False):
    print("De officiele Ordina pub-quiz antwoord vinder")
    model = Model(open('model/charList.txt').read())

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
            process_sheet(pages[p], model, save_image, sheet_name)

