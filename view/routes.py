from view import view
from view import db
from flask import render_template, request
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy

import main
import json

from view.models import Team
from view.models import TeamSchema
from view.models import Question
from view.models import QuestionSchema
from view.models import Category
from view.models import CategorySchema

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
    return jsonify(result);


@view.route('/api/v1.-/categories', methods=['GET'])
def get_categories():
    categories_schema = CategorySchema(many=True)
    allcategories = Category.query.all()
    result = categories_schema.dump(allcategories)
    return jsonify(result);


@view.route('/api/v1.0/newquestion', methods=['POST'])
def add_question():
    post = request.get_json();
    newquestion = post.get('question');
    newcorrect_answer = post.get('correct_answer');
    q = Question(question = newquestion, correct_answer = newcorrect_answer);
    db.session.add(q);
    db.session.commit();


@view.route('/run_program')
def run_program():
    line = main.test_test()
    # We wil use this url shortcut to start the program
    main.run_program()
    return line



