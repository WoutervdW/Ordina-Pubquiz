import unittest
import cv2
from app.word_segmentation import prepare_img, word_segmentation


class WordSegmentationTest(unittest.TestCase):
    def test_word_segmentation_scan1_line1(self):
        cv2.imread("test_files/line_files/scan1/scan1_line_1.png")
        self.assertEqual(True, True)

    def test_word_segmentation_scan1_line1(self):
        self.assertTrue(True)

