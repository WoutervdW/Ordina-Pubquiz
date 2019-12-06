from view import view, db
from flask import Flask, jsonify, render_template, abort, request, redirect, url_for, flash, make_response
from flask_sqlalchemy import SQLAlchemy
import main
import json
import random
import string
import datetime
import app
import cv2
import numpy as np
from view.models import Team, TeamSchema, Question, QuestionSchema, SubAnswer, SubAnswerSchema, Variant, VariantSchema, Category, CategorySchema, Answersheet, Person, \
 PersonSchema, Answer, AnswerSchema, SubAnswerGiven, SubAnswerGivenSchema, Word
from werkzeug.utils import secure_filename
from collections import OrderedDict


@view.route('/')
@view.route('/index')
def index():
    return render_template('index.html')


@view.route('/questions')
def questions():
    return render_template('questions.html')


@view.route('/answerchecking')
def answers():
    return render_template('answerchecking.html')


@view.route('/api/v1.0/teams', methods=['GET'])
def get_teams():
    teams_schema = TeamSchema(many=True)
    teams = Team.query.all()
    result = teams_schema.dump(teams)
    return jsonify(result)


@view.route('/api/v1.0/questions', methods=['GET'])
def get_questions():
    questions_schema = QuestionSchema(many=True)
    allquestions = Question.query.all()
    result = questions_schema.dump(allquestions)
    return jsonify(result)


@view.route('/api/v1.0/subanswers', methods=['GET'])
def get_subanswers():
    subanswers_schema = SubAnswerSchema(many=True)
    allsubanswers = SubAnswer.query.all()
    result = subanswers_schema.dump(allsubanswers)
    return jsonify(result)


@view.route('/api/v1.0/variants', methods=['GET'])
def get_variants():
    variant_schema = VariantSchema(many=True)
    allvariants = Variant.query.all()
    result = variant_schema.dump(allvariants)
    return jsonify(result)


@view.route('/api/v1.0/categories', methods=['GET'])
def get_categories():
    categories_schema = CategorySchema(many=True)
    allcategories = Category.query.all()
    result = categories_schema.dump(allcategories)
    return jsonify(result)


@view.route('/api/v1.0/persons', methods=['GET'])
def get_persons():
    persons_schema = PersonSchema(many=True)
    answers = Person.query.all()
    result = persons_schema.dump(answers)
    return jsonify(result)


@view.route('/api/v1.0/answers', methods=['GET'])
def get_answers():
    answers_schema = AnswerSchema(many=True)
    allanswers = Answer.query.all()
    result = answers_schema.dump(allanswers)
    return jsonify(result)


@view.route('/api/v1.0/subanswersgiven', methods=['GET'])
def get_subanswersgiven():
    subanswersgiven_schema = SubAnswerGivenSchema(many=True)
    allsubanswersgiven = SubAnswerGiven.query.all()
    result = subanswersgiven_schema.dump(allsubanswersgiven)
    return jsonify(result)


@view.route('/api/v1.0/newquestion', methods=['POST'])
def add_question():
    post = request.get_json();
    newquestion = post.get('question')
    newquestioncorrect_answer = post.get('correct_answer')
    newquestioncategory_id = post.get('category_id')
    newquestionperson_id = post.get('person_id')
    newquestionactive = post.get('active')
    q = Question(question=newquestion, correct_answer=newquestioncorrect_answer, category_id=newquestioncategory_id,
        person_id=newquestionperson_id, active=newquestionactive);
    db.session.add(q)
    db.session.commit()
    return


@view.route('/api/v1.0/updatequestion', methods=['POST'])
def update_question():
    post = request.get_json();
    id = post.get('id')
    questionactive = post.get('active')
    q = Question.query.filter_by(id=id).first()
    q.active = questionactive
    db.session.commit()
    return


@view.route('/api/v1.0/updateanswer', methods=['POST'])
def update_answer():
    post = request.get_json();
    id = post.get('id')
    answercorrect = post.get('correct')
    person_id = post.get('person_id')
    q = Answer.query.filter_by(id=id).first()
    q.correct = answercorrect
    q.person_id = person_id
    db.session.commit()
    return


@view.route('/run_program')
def run_program():
    # We wil use this url shortcut to start the program
    main.run_program()
    return "program finished"


@view.route('/answersheet/nuke', methods=['GET'])
def nuke_all_answersheets():
    Answersheet.query.delete()
    db.session.commit()
    db.engine.execute('alter sequence answersheet_id_seq RESTART with 1')
    return 'ok'


@view.route("/answersheet/save", methods=['GET', 'POST'])
def answersheet_save_all():
    # The image of a scan
    answer_images = app.save_answersheet()
    for answer_image in answer_images:
        # convert the image to byte array so it can be saved in the database
        answer = answer_image.tostring()
        # create an Image object to store it in the database
        # shape = answer_image
        width = len(answer_image)
        height = len(answer_image[0])
        new_answersheet = Answersheet(answersheet_image=answer, image_width=width, image_height=height)
        # add the object to the database session
        db.session.add(new_answersheet)
        # commit the session so that the image is stored in the database
        db.session.commit()
    return "answersheets saved"


@view.route("/load_answersheet/<int:question_id>", methods=['GET', 'POST'])
def load_answersheet(question_id):
    answersheet = Answersheet.query.filter_by(id=question_id).first()
    if answersheet is None:
        return "answersheet with id " + str(question_id) + " does not exist in the database."
    image_data = answersheet.answersheet_image
    # I need to know the exact shape it had in order to load it from the database
    width = answersheet.image_width
    height = answersheet.image_height
    np_answersheet = np.fromstring(image_data, np.uint8).reshape(width, height, 3)

    ret, png = cv2.imencode('.png', np_answersheet)
    response = make_response(png.tobytes())
    response.headers['Content-Type'] = 'image/png'
    return response


@view.route("/answersheet/load/<int:answersheet_id>", methods=['GET', 'POST'])
def answersheet_single(answersheet_id):
    return render_template("answersheet.html", answersheets=[answersheet_id])


@view.route("/answersheet/load", methods=['GET', 'POST'])
def answersheet_all():
    # TODO With large number of answersheets saved in the database make a 'next', 'previous' button functionality.
    page = request.args.get('page', 1, type=int)
    answersheets = Answersheet.query.paginate(page, view.config['ANSWERSHEET_PER_PAGE'], False)

    next_url = None
    if answersheets.has_next:
        next_url = url_for('answersheet_all', page=answersheets.next_num)

    prev_url = None
    if answersheets.has_prev:
        prev_url = url_for('answersheet_all', page=answersheets.prev_num)

    return render_template("answersheet.html", answersheets=answersheets.items, next_url=next_url, prev_url=prev_url)


@view.route('/answers/given/nuke', methods=['GET'])
def nuke_all_answers_given():
    SubAnswerGiven.query.delete()
    db.session.commit()
    db.engine.execute('alter sequence subanswergiven_id_seq RESTART with 1')
    return 'ok'


@view.route("/answers/given/load/<int:answer_given_id>", methods=['GET', 'POST'])
def load_answer(answer_given_id):
    print("loading given answer with id " + str(answer_given_id))
    answer_given = SubAnswerGiven.query.filter_by(id=answer_given_id).first()
    if answer_given is None:
        return "answer with id " + str(answer_given_id) + " does not exist in the database."
    image_data = answer_given.answer_image
    # I need to know the exact shape it had in order to load it from the database
    width = answer_given.image_width
    height = answer_given.image_height
    np_answer_given = np.fromstring(image_data, np.uint8).reshape(width, height, 3)

    ret, png = cv2.imencode('.png', np_answer_given)
    response = make_response(png.tobytes())
    response.headers['Content-Type'] = 'image/png'
    return response


@view.route("/answers/given/load", methods=['GET', 'POST'])
def answer_all():
    page = request.args.get('page', 1, type=int)
    answer_given_list = SubAnswerGiven.query.paginate(page, view.config['ANSWERS_GIVEN_PER_PAGE'], False)

    next_url = None
    if answer_given_list.has_next:
        next_url = url_for('answer_all', page=answer_given_list.next_num)

    prev_url = None
    if answer_given_list.has_prev:
        prev_url = url_for('answer_all', page=answer_given_list.prev_num)

    return render_template("answers_given.html", answers=answer_given_list.items, next_url=next_url, prev_url=prev_url)


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

