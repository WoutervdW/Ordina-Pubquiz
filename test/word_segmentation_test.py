import unittest
import os
import cv2
from app.word_segmentation import word_segmentation, prepare_image, show_image, find_rect
from app.line_segmentation import crop_and_warp


def check_line(path, l, line_word_count, scan_file):
    index = l.split("_")[-1]
    line = cv2.imread(path + l + "/center_" + index + ".png")
    original_height = line.shape[0]
    resized_height = 50
    line_original = line.copy()
    line = prepare_image(line, resized_height)
    res = word_segmentation(line, kernel_size=25, sigma=11, theta=7, min_area=100)

    # Save the words if this is not done so the result can be viewed to determine how it went wrong/good
    # If the folder does not exist yet we want to create it
    image_path = "test_files/word_files/" + scan_file + "/" + l
    if not os.path.exists(image_path):
        os.makedirs(image_path)

    multiply_factor = original_height / resized_height

    if len(os.listdir(image_path)) == 0:
        for (j, w) in enumerate(res):
            (word_box, word_img) = w
            (x, y, w, h) = word_box

            x_new = x * multiply_factor
            y_new = y * multiply_factor
            width_new = w * multiply_factor
            height_new = h * multiply_factor
            rect = find_rect(x_new, y_new, width_new, height_new)

            cropped = crop_and_warp(line_original, rect)
            cv2.imwrite(image_path + '/%d.png' % j, cropped)
            cv2.rectangle(line_original, (int(x_new), int(y_new)), (int(x_new + width_new), int(y_new + height_new)),
                          0, 1)

        # output summary image with bounding boxes
        cv2.imwrite(image_path + '/' + l + '_summary.png', line_original)

    if len(res) != line_word_count:
        # The test failed, print what went wrong and return False for the test
        print("line", l, "failed! It has", str(line_word_count), "words but the program found", len(res), "words")
        return False
    return True


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

