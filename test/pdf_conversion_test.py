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
        file_name = "scan1"
        pubquiz_answer_sheet = 'test_files/pdf_files/' + file_name + '.pdf'
        # For this test we only read 1 file
        answer_sheet_image = convert_pdf_to_image(pubquiz_answer_sheet)
        # We test to see if the shape of the pdf remains the same, we have calculated the shape for this file.
        # The conversion should give a colour image, which is the final parameter.
        # We test if the conversion is successful by seeing if the result is a double array with a colour parameter
        # If something went wrong it will not be a double array with rgb values so we give an error.
        self.assertEqual(len(answer_sheet_image[0][0]), 3)
        # If the test is successful we save the the image so we can use it in the next test
        if len(answer_sheet_image[0][0]) == 3 \
                and not os.path.isfile('test_files/image_files/' + file_name + '_image.png'):
            # We only save if the test was ok and the file does not exist yet.
            cv2.imwrite("test_files/image_files/" + file_name + "_image.png", answer_sheet_image)

    def test_wrong_file_path(self):
        file_name = "wrong_file_name"
        pubquiz_answer_sheet = 'test_files/pdf_files/' + file_name + '.pdf'
        # For this test we only read 1 file
        answer_sheet_image = convert_pdf_to_image(pubquiz_answer_sheet)
        self.assertEqual(answer_sheet_image, None)

    def test_no_pdf_file(self):
        file_name = "scan1"
        pubquiz_answer_sheet = 'test_files/image_files/' + file_name + '_image.png'
        answer_sheet_image = convert_pdf_to_image(pubquiz_answer_sheet)
        self.assertEqual(answer_sheet_image, None)


if __name__ == "__main__":
    test_pdf_to_image_conversion()

