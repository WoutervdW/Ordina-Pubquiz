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
from app.line_segmentation import line_segmentation
from app.word_segmentation import prepare_img, word_segmentation
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


def process_sheet(answer_sheet):
    # converts the pdf to the image based on the give path
    answer_sheet_image = convert_pdf_to_image(answer_sheet)

    gray = cv2.cvtColor(answer_sheet_image, cv2.COLOR_BGR2GRAY)
    # Now we have the answer sheet in image form and we can move on to the line segmentation
    lines = line_segmentation(gray)

    output_folder = "out"
    index = 0
    # After the line segmentation is done we can find the seperate words
    for line in lines:
        # read image, prepare it by resizing it to fixed height and converting it to grayscale
        # TODO The input images seem to be pre processed with a basic binary contrast
        #  (so black or white and no graytones) see if this is correct and if it will have an effect on our images
        # TODO remove the height, not needed I think
        # img = prepare_img(line, 180)
        # img = cv2.cvtColor(line, cv2.COLOR_BGR2GRAY)
        # execute segmentation with given parameters
        # -kernelSize: size of filter kernel (odd integer)
        # -sigma: standard deviation of Gaussian function used for filter kernel
        # -theta: approximated width/height ratio of words, filter function is distorted by this factor
        # - min_area: ignore word candidates smaller than specified area
        # TODO test out the theta and min_area parameter changes if the results are not good.
        res = word_segmentation(line, kernel_size=25, sigma=11, theta=7, min_area=100)
        print('Segmented into %d words' % len(res))
        print("for now just save everything to images")

        # iterate over all segmented words
        print('Segmented into %d words' % len(res))
        for (j, w) in enumerate(res):
            (word_box, word_img) = w
            (x, y, w, h) = word_box
            # save word
            cv2.imwrite(output_folder + '/' + str(index) + '.png', word_img)
            # draw bounding box in summary image
            cv2.rectangle(line, (x, y), (x + w, y + h), 0, 1)
            index += 1

        # output summary image with bounding boxes around words
        cv2.imwrite(output_folder + '/' + str(index) + 'summary.png', line)


def run(pubquiz_answer_sheets):
    print("De officiele Ordina pub-quiz antwoord vinder")

    for answer_sheet in pubquiz_answer_sheets:
        process_sheet(answer_sheet)

