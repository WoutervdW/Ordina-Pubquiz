import unittest
import os
from app.Model import Model
from app.sample_preprocessor import preprocess
from app.DataLoader import Batch
import cv2
from app.word_segmentation import show_image
import numpy as np


def test_word(scan_number, line_number, word_number, model):
    path = "test_files/word_files/scan_" \
           + str(scan_number) + "/line_" \
           + str(line_number) + "/words/word_" \
           + str(word_number) + ".png"

    word = cv2.imread(path)
    if word is not None:
        read_results = read_word_from_image(word, model)
        return read_results
    return None


def increase_contrast(img):
    # increase contrast
    pxmin = np.min(img)
    pxmax = np.max(img)
    imgContrast = (img - pxmin) / (pxmax - pxmin) * 255

    # increase line width
    kernel_contrast = np.ones((4, 4), np.uint8)
    imgMorph = cv2.erode(imgContrast, kernel_contrast, iterations=1)

    return imgMorph


def infer(_model, word_image):
    """
    recognize text in image provided by file path
    """
    fn_img = cv2.cvtColor(word_image, cv2.COLOR_BGR2GRAY)
    show_image(fn_img)
    # ret, fn_img = cv2.threshold(fn_img, 220, 255, cv2.THRESH_BINARY)
    fn_img = increase_contrast(fn_img)
    show_image(fn_img)
    image = preprocess(fn_img, Model.img_size)
    show_image(image)
    batch = Batch([image])
    (recognized, probability) = _model.infer_batch(batch, True)
    print('Recognized:', '"' + recognized[0] + '"')
    print('Probability:', probability[0])
    return recognized, probability


def read_word_from_image(image_to_read, model):
    results = infer(model, image_to_read)
    return results


class WordRecognitionTest(unittest.TestCase):
    def test_word_recognition(self):
        model = Model(open('../model/charList.txt').read(), "../model/")
        scan_number = 0
        line_number = 7
        word_number = 0
        print(test_word(scan_number, line_number, word_number, model))
        self.assertEqual(True, True)

    def test_all_words(self):
        model = Model(open('../model/charList.txt').read(), "../model/")
        scan_path = "test_files/word_files/"
        scans = [scans for scans in os.listdir(scan_path)]
        for scan in range(0, len(scans)):
            lines = [lines for lines in os.listdir(scan_path + scans[scan])]
            for line in range(0, len(lines)):
                words = [words for words in os.listdir(scan_path + scans[scan] + "/" + lines[line])]
                for word in range(0, len(words)):
                    print(test_word(scan, line, word, model))
        # If it arrives here without errors it has succesfully attempted to recoginize all words without errors
        self.assertTrue(True)

    def test_test_word(self):
        model = Model(open('../model/charList.txt').read(), "../model/")
        path = "test_words/B.PNG"

        word = cv2.imread(path)
        show_image(word)
        if word is not None:
            read_results = read_word_from_image(word, model)
            return read_results
        return None



