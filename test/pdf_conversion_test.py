import unittest
import os
from app.pdf_to_image import convert_pdf_to_image
import cv2


class PdfConversionTest(unittest.TestCase):
    def test_pdf_to_image_conversion(self):
        """
        converts the pdf to the image based on the give path.
        Check if the pdf is correctly converted.

        No test with multiple scans is included.
        If multiple scans are read they are converted individually. This is because we will have 2 separate files
        rather than 1 pdf with 2 pages so we would need to call the function twice regardless.
        """
        file_name = "Template_4"
        pubquiz_answer_sheet = '../original_scan/' + file_name + '.pdf'
        answer_sheets_image = convert_pdf_to_image(pubquiz_answer_sheet)
        # For this test we only read 1 file
        answer_sheet_image = answer_sheets_image[0]
        # The conversion should give a colour image, which is the final parameter.
        # We test if the conversion is successful by seeing if the result is a double array with a colour parameter
        # If something went wrong it will not be a double array with rgb values so we give an error.
        self.assertEqual(len(answer_sheet_image[0][0]), 3)

    def test_multiple_pdf_pages(self):
        file_name = "Template_4"
        path = '../original_scan/'
        pubquiz_answer_sheet = path + file_name + '.pdf'
        answer_sheets_image = convert_pdf_to_image(pubquiz_answer_sheet)

        self.assertEqual(len(answer_sheets_image), 2)

        # If the test is successful we save the the images if the folder is empty so we can use these in the next tests
        path = 'test_files/image_files/'
        if not os.path.exists(path):
            os.makedirs(path)
        if len(os.listdir(path)) == 0:
            for index in range(0, len(answer_sheets_image)):
                # We only save if the test was ok and the file does not exist yet.
                cv2.imwrite(path + file_name + "_" + str(index) + "_image.png", answer_sheets_image[index])

    def test_wrong_file_path(self):
        file_name = "wrong_file_name"
        pubquiz_answer_sheet = '../original_scan/' + file_name + '.pdf'
        # For this test we only read 1 file
        answer_sheet_image = convert_pdf_to_image(pubquiz_answer_sheet)
        self.assertEqual(answer_sheet_image, None)

    def test_no_pdf_file(self):
        file_name = "scan_0"
        pubquiz_answer_sheet = 'test_files/image_files/' + file_name + '_image.png'
        answer_sheet_image = convert_pdf_to_image(pubquiz_answer_sheet)
        self.assertEqual(answer_sheet_image, None)

