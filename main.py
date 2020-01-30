"""
A neural network that reads handwriting from given images.
Based on the project :
'build a handwritten text recognition system'
https://towardsdatascience.com/build-a-handwritten-text-recognition-system-using-tensorflow-2326a3487cd5
"""
import app
import os
from flask import render_template, redirect


def run_program(pubquiz_file_name):
    # TODO describe what is being done here.
    message = app.run_pubquiz_program(pubquiz_file_name)
    # After the files are processed we remove the file
    if os.path.exists(pubquiz_file_name):
        try:
            os.remove(pubquiz_file_name)
        finally:
            return message


