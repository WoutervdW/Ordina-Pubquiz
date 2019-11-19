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


if __name__ == "__main__":
    print("De officiele Ordina pub-quiz antwoord vinder")
    model = Model(open('model/charList.txt').read())

    image_to_read = ['test-images/handgeschreven_thick.png']
    # A simple example of how we could possibly use arguments to determine what image is tested
    # TODO make it better.
    for eachArg in sys.argv:
        image_to_read.append(eachArg)

    for image in image_to_read:
        infer(model, image)

    # # After the model is loaded we can very quickly load another image.
    # image_to_read_2 = 'test-images/tekst_thick.png'
    # infer(model, image_to_read_2)

