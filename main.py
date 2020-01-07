"""
A neural network that reads handwriting from given images.
Based on the project :
'build a handwritten text recognition system'
https://towardsdatascience.com/build-a-handwritten-text-recognition-system-using-tensorflow-2326a3487cd5
"""
import app
import os
from flask import redirect


def run_program(db, pubquiz_file_name):
    # We should be able to read all the files in a certain folder
    # os.listdir(input_folder) something like this.
    pubquiz_answer_sheets = [pubquiz_file_name]
    app.run_program(pubquiz_answer_sheets, True, db)

    # After the files are processed we remove the file
    if os.path.exists(pubquiz_file_name):
        os.remove(pubquiz_file_name)

    print("HOI SANDER")
    return redirect("http://www.example.com", code=302)


