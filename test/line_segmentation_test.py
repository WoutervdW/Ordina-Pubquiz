import unittest
import os
import cv2
from app.line_segmentation import line_segmentation


def read_number_of_lines(path, file_name):
    answer_sheet_image = cv2.imread(path + file_name + "_image.png")
    image_path = "test_files/line_files/"
    # If the folder does not exist yet we want to create it
    if not os.path.exists(image_path):
        os.makedirs(image_path)
    save_image = False
    if len(os.listdir(image_path)) == 0:
        # If the directory is empty then we want to save the lines that the test finds to the folder for the next tests
        save_image = True
    lines = line_segmentation(answer_sheet_image, save_image, image_path, file_name)
    return len(lines)


def read_line_ratios(path):
    lines = [line for line in os.listdir(path)]
    ratios = []
    for l in lines:
        # We want the number of the line. We use this quick trick
        # because the lines are saved with their prefix on the end
        index = l.split("_")[-1]
        # The lines are saved in separate folders and the line itself is the image with the center name
        line = cv2.imread(path + l + "/center_" + str(index) + ".png")
        height, width, _ = line.shape
        # The shape of the answer should always be about the same, namely about 180 pixels high and 2800 wide.
        # We will calculate the ratio of the line given and see if it is close enough to this bound.
        ratios.append([width / height, l])
    ratio_test = True
    # We assume that the width/height ratio is about 2800/180, so about 15.555 We will test on a rather loose bound.
    # TODO Change
    for ratio in ratios:
        if not 15 <= ratio[0] <= 16:
            # We test it like this rather than with a list comprehension because we want to print which line fails.
            print("line", ratio[1], "does not have the correct ratio. It's ratio is", ratio[0])
            ratio_test = False
    return ratio_test


class LineSegmentationTest(unittest.TestCase):

    # TODO Tests are written with hardcoded scans, which give the same tests but
    #  with 1 change in the and different results for different scans, maybe find a way to make this variable.
    def test_image_to_lines_scan1(self):
        """
        Converts the answer sheet image into separate lines. It reads an image provided by the previous test, in the
        real process it would just pass the image from memory and not save it.
        We do the test separate for scan1, 2 and 3. This is because each scan has a different number of lines that
        it should return and we want to test for the specific number of lines.
        """
        path = "test_files/image_files/"
        file_name = "scan_0"
        line_length = read_number_of_lines(path, file_name)
        self.assertEqual(line_length, 19)

    def test_image_to_lines_scan2(self):
        path = "test_files/image_files/"
        file_name = "scan_1"
        line_length = read_number_of_lines(path, file_name)
        # We don't count the big input field in this one, so we are looking for 23 lines.
        self.assertEqual(line_length, 23)

    def test_image_to_lines_scan3(self):
        path = "test_files/image_files/"
        file_name = "scan_2"
        line_length = read_number_of_lines(path, file_name)
        self.assertEqual(line_length, 27)

    def test_line_correctness_scan_0(self):
        """
        This tests if the found lines are all of the correct format. If this is not the case than something went wrong.
        This will read the line images from the previous tests so they are required to be run if the images are not
        in the folder. If they are not in the folder the test will succeed but nothing is tested.
        """
        path = "test_files/line_files/scan_0/"
        ratio_test = read_line_ratios(path)
        self.assertTrue(ratio_test)

    def test_line_correctness_scan_1(self):
        path = "test_files/line_files/scan_1/"
        ratio_test = read_line_ratios(path)
        self.assertTrue(ratio_test)

    def test_line_correctness_scan_2(self):
        path = "test_files/line_files/scan_2/"
        ratio_test = read_line_ratios(path)
        self.assertTrue(ratio_test)


