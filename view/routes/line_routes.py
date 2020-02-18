from view import view, db
from view.models import Line
from flask import request
from flask import make_response
from flask import render_template
from flask import url_for
import numpy as np
import cv2


@view.route('/lines/nuke', methods=['GET'])
def nuke_all_lines():
    Line.query.delete()
    db.session.commit()
    db.engine.execute('alter sequence line_id_seq RESTART with 1')
    return 'ok'


@view.route("/lines/load/<string:line_detail>", methods=['GET', 'POST'])
def load_lines(line_detail):
    print("loading given line with id " + str(line_detail))
    line_id = int(line_detail.split("_")[1])
    line = Line.query.filter_by(id=line_id).first()
    if line is None:
        return "answer with id " + str(line_id) + " does not exist in the database."
    image_data = line.line_image
    # I need to know the exact shape it had in order to load it from the database
    width = line.image_width
    height = line.image_height
    np_line = np.fromstring(image_data, np.uint8).reshape(width, height, 1)

    ret, png = cv2.imencode('.png', np_line)
    response = make_response(png.tobytes())
    response.headers['Content-Type'] = 'image/png'
    return response


@view.route("/lines/load/<int:line_id>", methods=['GET', 'POST'])
def load_lines_id(line_id):
    print("loading given line with id " + str(line_id))
    line = Line.query.filter_by(id=line_id).first()
    if line is None:
        return "answer with id " + str(line_id) + " does not exist in the database."
    image_data = line.line_image
    # I need to know the exact shape it had in order to load it from the database
    width = line.image_width
    height = line.image_height
    np_line = np.fromstring(image_data, np.uint8).reshape(width, height, 1)

    ret, png = cv2.imencode('.png', np_line)
    response = make_response(png.tobytes())
    response.headers['Content-Type'] = 'image/png'
    return response


@view.route("/lines/load", methods=['GET', 'POST'])
def lines_all():
    page = request.args.get('page', 1, type=int)
    line_list = Line.query.paginate(page, view.config['LINES_PER_PAGE'], False)

    next_url = None
    if line_list.has_next:
        next_url = url_for('lines_all', page=line_list.next_num)

    prev_url = None
    if line_list.has_prev:
        prev_url = url_for('lines_all', page=line_list.prev_num)

    return render_template("lines.html", lines=line_list.items, next_url=next_url, prev_url=prev_url)


@view.route("/get_answersheets_lines/<int:answersheet_id>", methods=['GET', 'POST'])
def get_answersheets_lines(answersheet_id):
    print("open answersheet with id " + str(answersheet_id))
    lines = Line.query.filter_by(answersheet_id=answersheet_id)
    return render_template("lines.html", lines=lines, next_url=None, prev_url=None)

