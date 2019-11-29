"""
A neural network that reads handwriting from given images.
Based on the project :
'build a handwritten text recognition system'
https://towardsdatascience.com/build-a-handwritten-text-recognition-system-using-tensorflow-2326a3487cd5
"""
import app


def test_test():
    return "Hoi Sander!"


def run():
    # We should be able to read all the files in a certain folder
    # os.listdir(input_folder) something like this.
    pubquiz_anser_sheets = ['scan.pdf']
    app.run(pubquiz_anser_sheets, True)

    print("HOI SANDER")

