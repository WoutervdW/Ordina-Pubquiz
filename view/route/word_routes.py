from view import view, db
from view.models import Word
from flask import request
from flask import make_response
from flask import render_template
from flask import url_for
import numpy as np
import cv2


@view.route('/words/nuke', methods=['GET'])
def nuke_all_words():
    Word.query.delete()
    db.session.commit()
    db.engine.execute('alter sequence word_id_seq RESTART with 1')
    return 'ok'


@view.route("/words/load/<int:word_id>", methods=['GET', 'POST'])
def load_word(word_id):
    print("loading given word with id " + str(word_id))
    word = Word.query.filter_by(id=word_id).first()
    if word is None:
        return "word with id " + str(word_id) + " does not exist in the database."
    image_data = word.word_image
    # I need to know the exact shape it had in order to load it from the database
    width = word.image_width
    height = word.image_height
    np_word = np.fromstring(image_data, np.uint8).reshape(width, height, 3)

    ret, png = cv2.imencode('.png', np_word)
    response = make_response(png.tobytes())
    response.headers['Content-Type'] = 'image/png'
    return response


@view.route("/words/load", methods=['GET', 'POST'])
def word_all():
    page = request.args.get('page', 1, type=int)
    word_list = Word.query.paginate(page, view.config['WORDS_PER_PAGE'], False)
    print("load %s words" % len(word_list.items))

    next_url = None
    if word_list.has_next:
        next_url = url_for('word_all', page=word_list.next_num)

    prev_url = None
    if word_list.has_prev:
        prev_url = url_for('word_all', page=word_list.prev_num)

    return render_template("words.html", words=word_list.items, next_url=next_url, prev_url=prev_url)

