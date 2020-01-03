import unittest
import os
import cv2
from app.word_segmentation import word_segmentation, prepare_image, show_image, find_rect, save_word_image
from app.line_segmentation import crop_and_warp


def check_line(path, l, line_word_count, scan_file, configurations=None, save_image=True):
    if configurations is None:
        # The standard configurations for the word segmentation
        configurations = [25, 11, 7, 100]
        # configurations = [19, 9, 5, 700]

    index = l.split("_")[-1]
    index = index.split(".png")[0]
    line_temp = cv2.imread(path + l)
    # This is kinda ugly, but the word segmentation expects 4 images, the center, 2 side boxes and the full line
    # We also stored an indication of which line it is after that, we will use the first image and the indication
    # of which line it is to save the images in the correct folders.
    line = [line_temp, index]
    original_height = line[0].shape[0]
    resized_height = 50

    line_analyse = line[0].copy()
    number_box_size = 65
    line_analyse = prepare_image(line_analyse, resized_height, number_box_size)
    res = word_segmentation(
        line_analyse,
        kernel_size=configurations[0],
        sigma=configurations[1],
        theta=configurations[2],
        min_area=configurations[3])

    if save_image:
        output_folder = "test_files/word_files/"
        multiply_factor = original_height / resized_height
        save_word_image(output_folder, scan_file, line, multiply_factor, res, number_box_size=number_box_size)

    # if len(res) != line_word_count:
    #     # The test failed, print what went wrong and return False for the test
    #     print("line", l, "failed! It has", str(line_word_count), "words but the program found", len(res), "words")
    #     return False
    return True


def test_single_line(scan_number, line_number, expected_word_count, configurations=None, save_image=True):
    """
    This tests a single given line. This can be used to tweak parameters when a line fails to find the
    correct number of words that you expected.
    """
    if configurations is None:
        configurations = [25, 11, 7, 100]

    path = "test_files/line_files/scan_" + str(scan_number) + "/"
    lines = [line for line in os.listdir(path)]

    return check_line(path, lines[line_number], expected_word_count, "scan_" + str(scan_number), configurations,
                      save_image)


# TODO Now the amount of lines and words are hardcoded for the 3 scans we used for testing. Make this configurable
class WordSegmentationTest(unittest.TestCase):

    def test_word_segmentation_scan_0_lines(self):
        path = "test_files/line_files/Template_4_0/"
        lines = [line for line in os.listdir(path)]
        # word_result = [1, 2, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
        # if len(lines) != len(word_result):
        #     print("Warning! There probably was an error in the line segmentation, fix that first before running this"
        #           " test. This test is based on the lines in scan1, if they are not correctly found the test could "
        #           "give false positives")
        #     self.assertEqual(len(lines), len(word_result))
        scan_0_word_test = True
        for x in range(0, len(lines)):
            if not check_line(path, lines[x], 2, "Template_4_0"):
                scan_0_word_test = False

        self.assertTrue(scan_0_word_test)

    def test_word_segmentation_scan_1_lines(self):
        path = "test_files/line_files/Template_4_1/"
        lines = [line for line in os.listdir(path)]
        # TODO @Sander: The ordering is off. It scans the folder and orders it (0, 1, 10, 11, ...2, 20, 21 etc.)
        # word_result = [2,  2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 7, 2, 2, 2, 3, 2, 2, 2, 1, 1, 1, 1, 1]
        # if len(lines) != len(word_result):
        #     print("Warning! There probably was an error in the line segmentation, fix that first before running this"
        #           " test. This test is based on the lines in scan1, if they are not correctly found the test could "
        #           "give false positives")
        #     self.assertEqual(len(lines), len(word_result))
        scan_1_word_test = True
        for x in range(0, len(lines)):
            if not check_line(path, lines[x], 2, "Template_4_1"):
                scan_1_word_test = False

        self.assertTrue(scan_1_word_test)

    def test_word_segmentation_scan_2_lines(self):
        path = "test_files/line_files/scan_2/"
        lines = [line for line in os.listdir(path)]
        # On scan2 there are some numbers and brackets and some number/word combination and one is empty
        word_result = [2, 3, 2, 2, 2, 2, 4, 1, 2, 4, 1, 2, 2, 4, 1, 2, 7, 2, 2, 7, 2, 3, 2, 2, 2, 2, 2]
        if len(lines) != len(word_result):
            print("Warning! There probably was an error in the line segmentation, fix that first before running this"
                  " test. This test is based on the lines in scan1, if they are not correctly found the test could "
                  "give false positives")
            self.assertEqual(len(lines), len(word_result))
        scan_2_word_test = True
        for x in range(0, len(lines)):
            if not check_line(path, lines[x], word_result[x], "scan_2"):
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

    def test_parameter_range(self):
        """
        This test will run until it finds a combination of parameters (within your range) for which it finds the correct
        amount of words. If no configuration exists within your range it returns false.
        It will test all the lines of a given scan
        """
        scan_number = 0
        path = "test_files/line_files/scan_" + str(scan_number)
        lines = [line for line in os.listdir(path)]
        # The expected word count is 2 for all the lines in scan 0. Change this for different scans to be an array.
        expected_word_count = 2
        # k should be odd
        for k in range(19, 30, 2):
            print("TEST: " + str(k) + " out of 30")
            # s should be positive
            for s in range(9, 15):
                # t should be positive
                for t in range(5, 12):
                    for m in range(100, 1000, 100):
                        configurations = [k, s, t, m]
                        # We will run the configuration for all the lines.
                        correct_lines = 0
                        for l in range(0, len(lines)):
                            if test_single_line(scan_number, l, expected_word_count, configurations, save_image=False):
                                correct_lines += 1
                        if correct_lines == len(lines):
                            print("k: " + str(k) + " s: " + str(s) + " t: " + str(t) + " m: " + str(m))
                            self.assertTrue(True)
        # If it comes here the test failed.
        self.assertTrue(False)
