import unittest
import os
from app.Model import Model
from app.SamplePreprocessor import preprocess
from app.DataLoader import Batch
import cv2


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


class WordRecognitionTest(unittest.TestCase):
    def test_word_recognition(self):
        model = Model(open('../model/charList.txt').read(), "../model/")
        scan_number = 0
        line_number = 0
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




