from view import view
from flask import render_template
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
import main

from view.models import Team
from view.models import TeamSchema
from view.models import Question
from view.models import QuestionSchema

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


@view.route('/run_program')
def run_program():
    line = main.test_test()
    # We wil use this url shortcut to start the program
    main.run_program()
    return line



