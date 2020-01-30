from view import view
from flask import request, render_template
from werkzeug.utils import secure_filename
import main
from multiprocessing.pool import ThreadPool


@view.route('/uploader', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        print("saving file!")
        f = request.files['answersheets']
        # We wil use this url shortcut to start the program
        # Set the next thread to happen
        f.save(secure_filename(f.filename))
        pool = ThreadPool(processes=1)
        async_result = pool.apply_async(main.run_program, (f.filename,))
        message = async_result.get()
        return render_template('answerchecking.html', message=message)

