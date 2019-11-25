import unittest
import os
import cv2
from app.word_segmentation import word_segmentation


def check_line(path, l, line_word_count, scan_file):
    line = cv2.imread(path + l)
    res = word_segmentation(line, kernel_size=25, sigma=11, theta=7, min_area=100)

    # Save the words if this is not done so the result can be viewed to determine how it went wrong/good
    print('Segmented into %d words' % len(res))
    # If the folder does not exist yet we want to create it ([:-4] is a quick and dirty way to remove the extension)
    image_path = "test_files/word_files/" + scan_file + "/" + l[:-4]
    if not os.path.exists(image_path):
        os.makedirs(image_path)

    if len(os.listdir(image_path)) == 0:
        # If the directory is empty then we want to save the words that the test finds.
        for (j, w) in enumerate(res):
            (word_box, word_img) = w
            (x, y, w, h) = word_box
            # save word
            cv2.imwrite(image_path + '/%d.png' % j, word_img)
            # draw bounding box in summary image
            cv2.rectangle(line, (x, y), (x + w, y + h), 0, 1)

        # output summary image with bounding boxes
        cv2.imwrite(image_path + '/' + l[:-4] + '_summary.png', line)

    if len(res) != line_word_count:
        # The test failed, print what went wrong and return False for the test
        print("line", l, "failed! It has", line_word_count, "words but the program found", len(res), "words")
        return False
    return True


class WordSegmentationTest(unittest.TestCase):

    # TODO Similar to lines this can be made variable. The input and the result are different depending on the scan
    #  The user should be able to change the test with his own input and result
    def test_word_segmentation_scan1_lines(self):
        path = "test_files/line_files/scan1/"
        lines = [line for line in os.listdir(path)]
        # TODO @Sander: The ordering is off. It scans the folder and orders it (1, 10, 11, ...2, 20, 21 etc.)
        # On scan1 there are all names, so 19 answers and 2 words for each lines
        word_result = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
        if len(lines) != len(word_result):
            print("Warning! There probably was an error in the line segmentation, fix that first before running this"
                  " test. This test is based on the lines in scan1, if they are not correctly found the test could "
                  "give false positives")
            self.assertEqual(len(lines), len(word_result))
        scan1_word_test = True
        for x in range(0, len(lines)):
            if not check_line(path, lines[x], word_result[x], "scan1"):
                scan1_word_test = False

        self.assertTrue(scan1_word_test)

    def test_word_segmentation_scan2_lines(self):
        path = "test_files/line_files/scan2/"
        lines = [line for line in os.listdir(path)]
        # TODO @Sander: The ordering is off. It scans the folder and orders it (1, 10, 11, ...2, 20, 21 etc.)
        # On scan2 there are some numbers and brackets and some number/word combination and one is empty
        word_result = [7, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2]
        if len(lines) != len(word_result):
            print("Warning! There probably was an error in the line segmentation, fix that first before running this"
                  " test. This test is based on the lines in scan1, if they are not correctly found the test could "
                  "give false positives")
            self.assertEqual(len(lines), len(word_result))
        scan2_word_test = True
        for x in range(0, len(lines)):
            if not check_line(path, lines[x], word_result[x], "scan2"):
                scan2_word_test = False

        self.assertTrue(scan2_word_test)

    def test_word_segmentation_scan3_lines(self):
        path = "test_files/line_files/scan3/"
        lines = [line for line in os.listdir(path)]
        # On scan2 there are some numbers and brackets and some number/word combination and one is empty
        word_result = [2, 2, 2, 2, 4, 1, 2, 4, 1, 2, 4, 2, 1, 2, 7, 2, 2, 7, 2, 2, 3, 2, 2, 2, 2, 2, 2]
        if len(lines) != len(word_result):
            print("Warning! There probably was an error in the line segmentation, fix that first before running this"
                  " test. This test is based on the lines in scan1, if they are not correctly found the test could "
                  "give false positives")
            self.assertEqual(len(lines), len(word_result))
        scan3_word_test = True
        for x in range(0, len(lines)):
            if not check_line(path, lines[x], word_result[x], "scan3"):
                scan3_word_test = False

        self.assertTrue(scan3_word_test)


