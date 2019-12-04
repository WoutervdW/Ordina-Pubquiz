from view import view, db
from flask import render_template, request, Flask, abort, jsonify
from flask_sqlalchemy import SQLAlchemy

import main
import json
import random
import string
import datetime
import app
import cv2
import numpy as np

from view.models import Team
from view.models import TeamSchema
from view.models import Question
from view.models import QuestionSchema
from view.models import Category
from view.models import CategorySchema
from view.models import User
from view.models import UserSchema
from view.models import Image

from collections import OrderedDict


@view.route('/')
@view.route('/index')
@view.route('/sander')
def index():
    return render_template('index.html')


@view.route('/questions')
def questions():
    return render_template('questions.html')


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


@view.route('/api/v1.0/categories', methods=['GET'])
def get_categories():
    categories_schema = CategorySchema(many=True)
    allcategories = Category.query.all()
    result = categories_schema.dump(allcategories)
    return jsonify(result)


@view.route('/api/v1.0/users', methods=['GET'])
def get_users():
    users_schema = UserSchema(many=True)
    allusers = User.query.all()
    result = users_schema.dump(allusers)
    return jsonify(result)


@view.route('/api/v1.0/newquestion', methods=['POST'])
def add_question():
    post = request.get_json();
    newquestion = post.get('question')
    newquestioncorrect_answer = post.get('correct_answer')
    newquestioncategory_id = post.get('category_id')
    newquestionuser_id = post.get('user_id')
    newquestionactive = post.get('active')
    q = Question(question=newquestion, correct_answer=newquestioncorrect_answer, category_id=newquestioncategory_id, user_id=newquestionuser_id, active=newquestionactive);
    db.session.add(q)
    db.session.commit()


@view.route('/api/v1.0/updatequestion', methods=['POST'])
def update_question():
    post = request.get_json();
    id = post.get('id')
    #question = post.get('question')
    #questioncorrect_answer = post.get('correct_answer')
    #questioncategory_id = post.get('category_id')
    #questionuser_id = post.get('user_id')
    questionactive = post.get('active')
    q = Question.query.filter_by(id=id).first()
    #q.question = question
    #q.correct_answer = questioncorrect_answer
    #q.category_id = questioncategory_id
    #q.user_id = questionuser_id
    q.active = questionactive
    db.session.commit()


@view.route('/run_program')
def run_program():
    line = main.test_test()
    # We wil use this url shortcut to start the program
    main.run_program()
    return line

@view.route('/images/nuke', methods=['GET'])
def nuke_all_images():
    Image.query.delete()
    db.session.commit()
    db.engine.execute('alter sequence images_id_seq RESTART with 1')
    return 'ok'


@view.route("/test_answersheet_save", methods=['GET', 'POST'])
def test_answersheet_save():
    # The image of a scan
    answer_image = app.save_answersheet()
    # convert the image to byte array so it can be saved in the database
    answer = answer_image.tostring()
    # create an Image object to store it in the database
    new_image = Image(name='test', img_filename=None, img_data=answer)
    # add the object to the database session
    db.session.add(new_image)
    # commit the session so that the image is stored in the database
    db.session.commit()
    return "test successful"


@view.route("/test_answersheet_load", methods=['GET', 'POST'])
def test_answersheet_load():
    images = Image.query.all()
    images = list(filter(lambda img: img.img_data != None, images))
    # We get a list of all the images in the database, we only take 1 to show.
    image = images[0]
    image_data = image.img_data
    # I need to know the exact shape it had in order to load it from the database
    nparr = np.fromstring(image_data, np.uint8).reshape(5848, 4139, 3)

    # Test to see if it correctly shows the image (it does)
    # cv2.imwrite('test.png', nparr)

    ret, png = cv2.imencode('.png', nparr)
    response = make_response(png.tobytes())
    response.headers['Content-Type'] = 'image/png'
    return response

