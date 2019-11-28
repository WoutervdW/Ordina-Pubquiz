import unittest
import os
import cv2
from app.word_segmentation import word_segmentation, prepare_image, show_image, find_rect, save_word_image
from app.line_segmentation import crop_and_warp


def check_line(path, l, line_word_count, scan_file, configurations=None):

    if configurations is None:
        # The standard configurations for the word segmentation
        # configurations = [25, 11, 7, 100]
        configurations = [25, 11, 7, 100]

    index = l.split("_")[-1]
    line_temp = cv2.imread(path + l + "/center_" + index + ".png")
    # This is kinda ugly, but the word segmentation expects 4 images, the center, 2 side boxes and the full line
    # We also stored an indication of which line it is after that, we will use the first image and the indication
    # of which line it is to save the images in the correct folders.
    line = [line_temp, 0, 0, 0, index]
    original_height = line[0].shape[0]
    resized_height = 50

    line_analyse = line[0].copy()
    line_analyse = prepare_image(line_analyse, resized_height)
    res = word_segmentation(
        line_analyse,
        kernel_size=configurations[0],
        sigma=configurations[1],
        theta=configurations[2],
        min_area=configurations[3])

    output_folder = "test_files/word_files/"
    multiply_factor = original_height / resized_height

    save_word_image(output_folder, scan_file, line, multiply_factor, res)
    if len(res) != line_word_count:
        # The test failed, print what went wrong and return False for the test
        print("line", l, "failed! It has", str(line_word_count), "words but the program found", len(res), "words")
        return False
    return True


def test_single_line(scan_number, line_number, expected_word_count, configurations=None):
    """
    This tests a single given line. This can be used to tweak parameters when a line fails to find the
    correct number of words that you expected.
    """
    if configurations is None:
        configurations = [25, 11, 7, 100]

    path = "test_files/line_files/scan_" + str(scan_number) + "/"
    lines = [line for line in os.listdir(path)]

    return check_line(path, lines[line_number], expected_word_count, "scan_" + str(scan_number), configurations)


class WordSegmentationTest(unittest.TestCase):

    # TODO Similar to lines this can be made variable. The input and the result are different depending on the scan
    #  The user should be able to change the test with his own input and result
    def test_word_segmentation_scan_0_lines(self):
        path = "test_files/line_files/scan_0/"
        lines = [line for line in os.listdir(path)]
        # On scan_0 there are all names, so 19 answers and 2 words for each lines
        word_result = {1: 2,
                       2: 2,
                       3: 2,
                       4: 2,
                       5: 2,
                       6: 2,
                       7: 2,
                       8: 2,
                       9: 2,
                       10: 2,
                       11: 2,
                       12: 2,
                       13: 2,
                       14: 2,
                       15: 2,
                       16: 2,
                       17: 2,
                       18: 2,
                       19: 2}
        if len(lines) != len(word_result):
            print("Warning! There probably was an error in the line segmentation, fix that first before running this"
                  " test. This test is based on the lines in scan1, if they are not correctly found the test could "
                  "give false positives")
            self.assertEqual(len(lines), len(word_result))
        scan_0_word_test = True
        for x in range(0, len(lines)):
            if not check_line(path, lines[x], word_result[x+1], "scan_0"):
                scan_0_word_test = False

        self.assertTrue(scan_0_word_test)

    def test_word_segmentation_scan_1_lines(self):
        path = "test_files/line_files/scan_1/"
        lines = [line for line in os.listdir(path)]
        # TODO @Sander: The ordering is off. It scans the folder and orders it (1, 10, 11, ...2, 20, 21 etc.)
        # On scan_1 there are some numbers and brackets and some number/word combination and one is empty
        word_result = {1: 2,
                       2: 1,
                       3: 1,
                       4: 1,
                       5: 1,
                       6: 1,
                       7: 1,
                       8: 1,
                       9: 1,
                       10: 1,
                       11: 1,
                       12: 2,
                       13: 1,
                       14: 2,
                       15: 2,
                       16: 2,
                       17: 3,
                       18: 2,
                       19: 7,
                       20: 2,
                       21: 2,
                       22: 1,
                       23: 1,
                       24: 1,
                       25: 1}
        if len(lines) != len(word_result):
            print("Warning! There probably was an error in the line segmentation, fix that first before running this"
                  " test. This test is based on the lines in scan1, if they are not correctly found the test could "
                  "give false positives")
            self.assertEqual(len(lines), len(word_result))
        scan_1_word_test = True
        for x in range(0, len(lines)):
            if not check_line(path, lines[x], word_result[x + 1], "scan_1"):
                scan_1_word_test = False

        self.assertTrue(scan_1_word_test)

    def test_word_segmentation_scan_2_lines(self):
        path = "test_files/line_files/scan_2/"
        lines = [line for line in os.listdir(path)]
        # On scan2 there are some numbers and brackets and some number/word combination and one is empty
        word_result = {1: 2,
                       2: 3,
                       3: 2,
                       4: 2,
                       5: 2,
                       6: 2,
                       7: 2,
                       8: 2,
                       9: 2,
                       10: 2,
                       11: 2,
                       12: 2,
                       13: 2,
                       14: 2,
                       15: 4,
                       16: 1,
                       17: 2,
                       18: 4,
                       19: 1,
                       20: 2,
                       21: 4,
                       22: 1,
                       23: 2,
                       24: 7,
                       25: 2,
                       26: 2,
                       27: 7}
        if len(lines) != len(word_result):
            print("Warning! There probably was an error in the line segmentation, fix that first before running this"
                  " test. This test is based on the lines in scan1, if they are not correctly found the test could "
                  "give false positives")
            self.assertEqual(len(lines), len(word_result))
        scan_2_word_test = True
        for x in range(0, len(lines)):
            if not check_line(path, lines[x], word_result[x + 1], "scan_2"):
                scan_2_word_test = False

        self.assertTrue(scan_2_word_test)

    def test_word_segmentation_single_line(self):
        """
        This tests a single given line. This can be used to tweak parameters when a line fails to find the
        correct number of words that you expected.
        """
        scan_number = 0
        # The lines are taken from the folder in the order: 0, 1, 10, 11, 12, 13, 14, 15, 16, 17, 18, 2, 3, 4, 5, 6,
        # 7, 8, 9 (scan_0 example). Please take this into account when choosing a line number. Sorry.
        line_number = 2
        expected_word_count = 2

        configurations = [25, 11, 7, 100]
        self.assertTrue(test_single_line(scan_number, line_number, expected_word_count, configurations))

