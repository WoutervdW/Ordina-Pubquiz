from view import view, db
from flask import request, redirect, url_for
from werkzeug.utils import secure_filename
import threading
import main


@view.route('/uploader', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        print("saving file!")
        f = request.files['answersheets']
        # We wil use this url shortcut to start the program
        # Set the next thread to happen
        print("starting thread for program")
        f.save(secure_filename(f.filename))
        x = threading.Thread(target=main.run_program, args=(db, f.filename,))
        print("thread started")
        x.start()

        x.join()
        return redirect(url_for('answers'),  code=302)