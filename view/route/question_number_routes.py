from view import view, db
from view.models import QuestionNumber
from flask import request
from flask import make_response
from flask import render_template
from flask import url_for
import numpy as np
import cv2


@view.route('/questions/nuke', methods=['GET'])
def nuke_all_questions():
    QuestionNumber.query.delete()
    db.session.commit()
    db.engine.execute('alter sequence questionnumber_id_seq RESTART with 1')
    return 'ok'


@view.route("/questions/load/<string:question_detail>", methods=['GET', 'POST'])
def load_questions(question_detail):
    print("loading given question number with id " + str(question_detail))
    question_id = int(question_detail.split("_")[1])
    question = QuestionNumber.query.filter_by(id=question_id).first()
    if question is None:
        return "question with id " + str(question_id) + " does not exist in the database."
    image_data = question.question_image
    # I need to know the exact shape it had in order to load it from the database
    width = question.image_width
    height = question.image_height
    np_question = np.fromstring(image_data, np.uint8).reshape(width, height, 3)

    ret, png = cv2.imencode('.png', np_question)
    response = make_response(png.tobytes())
    response.headers['Content-Type'] = 'image/png'
    return response


@view.route("/questions/load/<int:question_id>", methods=['GET', 'POST'])
def load_question_id(question_id):
    print("loading given question with id " + str(question_id))
    question = QuestionNumber.query.filter_by(id=question_id).first()
    if question is None:
        return "question with id " + str(question_id) + " does not exist in the database."
    image_data = question.question_image
    # I need to know the exact shape it had in order to load it from the database
    width = question.image_width
    height = question.image_height
    # We now have '1' instead of '3' because the image now is grayscale
    np_question = np.fromstring(image_data, np.uint8).reshape(width, height, 1)

    ret, png = cv2.imencode('.png', np_question)
    response = make_response(png.tobytes())
    response.headers['Content-Type'] = 'image/png'
    return response


@view.route("/questions/load", methods=['GET', 'POST'])
def questions_all():
    page = request.args.get('page', 1, type=int)
    question_list = QuestionNumber.query.paginate(page, view.config['QUESTIONS_PER_PAGE'], False)
    print(len(question_list.items))

    next_url = None
    if question_list.has_next:
        next_url = url_for('questions_all', page=question_list.next_num)

    prev_url = None
    if question_list.has_prev:
        prev_url = url_for('questions_all', page=question_list.prev_num)

    return render_template("question_numbers.html", questions=question_list.items, next_url=next_url, prev_url=prev_url)

