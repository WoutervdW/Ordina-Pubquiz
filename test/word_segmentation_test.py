import unittest
import os
import cv2
from app.word_segmentation import word_segmentation, prepare_image, show_image
from app.line_segmentation import crop_and_warp


def find_rect(x, y, w, h):
    top_left = [x, y+h]
    top_right = [x+w, y+h]
    bottom_right = [x+w, y]
    bottom_left = [x, y]
    return [bottom_left, bottom_right, top_right, top_left]


def print_word(original_image, image_path, res, resized_height, original_height):
    if not os.path.exists(image_path):
        os.makedirs(image_path)
    # If the directory is empty then we want to save the words that the test finds.
    multiply_factor = original_height/resized_height
    for (j, w) in enumerate(res):
        (word_box, word_img) = w
        (x, y, w, h) = word_box
        x_new = x * multiply_factor
        y_new = y * multiply_factor
        width_new = w * multiply_factor
        height_new = h * multiply_factor
        rect = find_rect(x_new, y_new, width_new, height_new)

        cropped = crop_and_warp(original_image, rect)
        cv2.imwrite(image_path + '/%d.png' % j, cropped)
        cv2.rectangle(original_image, (int(x_new), int(y_new)), (int(x_new+width_new), int(y_new+height_new)), 0, 1)
        # show_image(cropped)
        
    cv2.imwrite(image_path + '/summary.png', original_image)


def check_line(path, l, line_word_count, scan_file):
    index = l.split("_")[-1]
    line = cv2.imread(path + l + "/center_" + index + ".png")
    res = word_segmentation(line, kernel_size=25, sigma=11, theta=7, min_area=100)

    # Save the words if this is not done so the result can be viewed to determine how it went wrong/good
    print('Segmented into %d words' % len(res))
    # If the folder does not exist yet we want to create it
    image_path = "test_files/word_files/" + scan_file + "/" + l
    if not os.path.exists(image_path):
        os.makedirs(image_path)

    if len(os.listdir(image_path)) == 0:
        for (j, w) in enumerate(res):
            (word_box, word_img) = w
            (x, y, w, h) = word_box
            # save word
            cv2.imwrite(image_path + '/%d.png' % j, word_img)
            # draw bounding box in summary image
            cv2.rectangle(line, (x, y), (x + w, y + h), 0, 1)

        # output summary image with bounding boxes
        cv2.imwrite(image_path + '/' + l + '_summary.png', line)

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

    def test_one(self):
        if not os.path.exists("test_files/line_test/"):
            os.makedirs("test_files/line_test/")
        path = "test_files/line_files/scan_0/"
        lines = [line for line in os.listdir(path)]
        index = lines[1].split("_")[-1]
        original_image = cv2.imread(path + lines[1] + "/center_" + index + ".png")
        line = original_image.copy()
        # play around with different parameters per line.
        index = 0
        # for k in range(0, 20):
        #     for s in range(11, 12):
        #         print("test: " + str(k) + " out of 20")
        #         for t in range(0, 20):
        # First we see the effect of changing 1 variable
        # K: 1->201 => 7, 9, .. 10, 10, 9, 9, 8, 8, 7 .... to 7 in about 10 and stayed there.
        # S: 1 -> 101 => 1, 9, 10, 9, 9, .... to 9 fast and stayed there.
        # T: 1 -> 101 => 9, 10, 9 and stayed there.
        # M: 1000 -> 11000
        k = 25
        s = 11
        t = 7
        m = 100

        sigma = s
        kernel_size = k
        # The second test is increasing the sigma
        # The third test is increasing the theta
        theta = t
        # The fourth test is increasing the min_area. This is done with 100 increments
        min_area = m
        original_height = line.shape[0]
        resized_height = 50
        line = prepare_image(line, resized_height)
        res = word_segmentation(line, kernel_size=kernel_size, sigma=sigma, theta=theta, min_area=min_area)
        print(len(res))
        word_info = "index " + str(index) + ": result found with paramater: "
        word_info = word_info + "kernel size: " + str(kernel_size) + "; "
        word_info = word_info + "sigma: " + str(sigma) + "; "
        word_info = word_info + "theta: " + str(theta) + "; "
        word_info = word_info + "min_area: " + str(min_area) + "; \n"

        image_path = "test_files/line_test/" + lines[1]
        print_word(original_image, image_path, res, resized_height=resized_height, original_height=original_height)
        print(word_info)
        index += 1

    def test_all(self):
        # We will use this to test a bunch of different parameters and see which give the closest result.
        # Only a small kernel seems to have a negative effect on how many words are found.
        # With large kernels the result remains steady.
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
        if not os.path.exists("test_results/"):
            os.makedirs("test_results/")
        # f = []
        # for l in range(0, len(lines)):
        #     f.append(open('test_results/line_' + str(l+1) + ".txt", 'w'))

        # play around with different parameters per line.
        for k in range(0, 50):
            for s in range(0, 50):
                print("test: " + str(k) + " out of 100")
                for t in range(0, 50):
                    for m in range(1, 50):
                        # The first tests is how the kernel improves if it is increased. It has to be an odd number
                        kernel_size = 1 + (k*2)
                        # The second test is increasing the sigma
                        sigma = 11+s
                        # The third test is increasing the theta
                        theta = t+1
                        # The fourth test is increasing the min_area. This is done with 100 increments
                        min_area = (m * 100)

                        # For the first scan all the answers should be 2, which makes it easy for us.
                        line_word = []
                        for l in range(0, len(lines)):
                            index = lines[0].split("_")[-1]
                            line = cv2.imread(path + lines[0] + "/center_" + index + ".png")
                            res = word_segmentation(line, kernel_size=kernel_size, sigma=sigma, theta=theta, min_area=min_area)

                            # print('It found ' + str(len(res)) + ' words and it should have ' + str(2))
                            line_word.append(len(res))
                        correct = True
                        for words in line_word:
                            if words != 2:
                                correct = False

                        if correct:
                            word_info = "result found with paramater: "
                            word_info = word_info + "kernel size: " + str(kernel_size) + "; "
                            word_info = word_info + "sigma: " + str(sigma) + "; "
                            word_info = word_info + "theta: " + str(theta) + "; "
                            word_info = word_info + "min_area: " + str(min_area) + "; "

                            print(word_info)
                            # if len(res) == 2:
                            #     index = 0
                            #
                            #     print("line: " + lines[0], file=f[l])
                            #     for (j, w) in enumerate(res):
                            #         word_info = "word " + str(index) + "=>"
                            #         word_info = word_info + "kernel size: " + str(kernel_size) + "; "
                            #         word_info = word_info + "sigma: " + str(sigma) + "; "
                            #         word_info = word_info + "theta: " + str(theta) + "; "
                            #         word_info = word_info + "min_area: " + str(min_area) + "; "
                            #
                            #         (word_box, word_img) = w
                            #         (x, y, w, h) = word_box
                            #
                            #         area = (w*h)
                            #         word_info = word_info + "actual area: " + str(area) + "; "
                            #         print(word_info, file=f[l])
                                # print("accurate!")

        # for l in range(0, len(lines)):
        #     f[l].close()
