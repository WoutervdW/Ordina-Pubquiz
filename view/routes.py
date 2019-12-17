from view import view, db
from flask import Flask, jsonify, render_template, abort, request, redirect, url_for, flash, make_response, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, distinct
import main
import json
import random
import string
import datetime
import app
import cv2
import numpy as np
from view.models import Team, TeamSchema, Question, QuestionSchema, SubAnswer, SubAnswerSchema, Variant, VariantSchema, Category, CategorySchema, Answersheet, Person, \
PersonSchema, SubAnswerGiven, SubAnswerGivenSchema, Word
from werkzeug.utils import secure_filename
from collections import OrderedDict
import threading
from view import route


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


@view.route('/uploadsheets')
def uploadsheets():
    return render_template('uploadsheets.html')


@view.route('/revealwinner')
def reveal():
    return render_template('revealwinner.html')


@view.route('/login')
def login():
    if session['logged_in']:
        return render_template('index.html')
    return render_template('login.html')


@view.route('/api/v1.0/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    user = Person.query.filter_by(personname=username).first()
    if user and user.check_password(password):
        session['logged_in'] = True
        session['userid'] = user.id
        return redirect(url_for('index'))
    else:
        if user:
            flash('Wachtwoord klopt niet')
        else:
            flash('Gebruiker bestaat niet')
        return login()


@view.route("/logout")
def logout():
    session['logged_in'] = False
    return login()


@view.route('/api/v1.0/teams', methods=['GET'])
def get_teams():
    scores = db.session.query(SubAnswerGiven.team_id, func.count(SubAnswerGiven.id).label('score')).group_by(SubAnswerGiven.team_id).filter(SubAnswerGiven.correct).all()
    teams = Team.query.all()
    teams_schema = TeamSchema(many=True)
    for team in teams:
        team.score = 0
        for i in range(0, len(scores)):
            teamid = scores[i][0]
            if team.id == teamid:
                team.score = scores[i][1]
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


@view.route('/api/v1.0/persons', methods=['GET'])
def get_persons():
    persons_schema = PersonSchema(many=True)
    people = Person.query.all()
    result = persons_schema.dump(people)
    return jsonify(result)


@view.route('/api/v1.0/subanswers', methods=['GET'])
def get_answers():
    answers_schema = SubAnswerGivenSchema(many=True)
    allanswers = SubAnswerGiven.query.all()
    result = answers_schema.dump(allanswers)
    return jsonify(result)


@view.route('/api/v1.0/newquestion', methods=['POST'])
def add_question():
    post = request.get_json()
    newquestion = post.get('question')
    newsubanswers = post.get('subanswers')
    subanswers = []
    variants = []
    for i in range(0, len(newsubanswers)):
        for j in range(0, len(newsubanswers[i]['variants'])):
            variant = Variant(answer=newsubanswers[i]['variants'][j]['answer'])
            variants.append(variant);
        subanswer = SubAnswer(variants=variants)
        subanswers.append(subanswer)
        variants = []
    newquestioncategory = post.get('category')
    category = Category.query.filter(Category.name == newquestioncategory).first()
    print(category)
    if category is None:
        category = Category(name=newquestioncategory)

    newquestionperson_id = session['userid']
    newquestionactive = post.get('active')
    q = Question(question=newquestion, questioncategory=category,
        person_id=newquestionperson_id, active=newquestionactive, subanswers=subanswers)
    db.session.add(q)
    db.session.commit()
    return 'OK'


@view.route('/api/v1.0/updatequestion', methods=['POST'])
def update_question():
    post = request.get_json()
    id = post.get('id')
    q = Question.query.filter_by(id=id).first()
    if post.get('active') is not None:
        questionactive = post.get('active')
        q.active = questionactive

    if post.get('questionnumber') is not None:
        questionnumber = int(post.get('questionnumber'))
        while True:
            qtemp = Question.query.filter_by(questionnumber=questionnumber).first()
            if qtemp is None:
                q.questionnumber = questionnumber
                break
            else:
                if qtemp.id == id:
                    break
                questionnumber = questionnumber + 1
    db.session.commit()
    return 'OK'


@view.route('/api/v1.0/removequestion', methods=['POST'])
def remove_question():
    post = request.get_json()
    id = post.get('id')
    subanswers = SubAnswer.query.filter_by(question_id=id).all()
    for subanswer in subanswers:
        Variant.query.filter_by(subanswer_id=subanswer.id).delete()
    SubAnswer.query.filter_by(question_id=id).delete()
    Question.query.filter_by(id=id).delete()
    db.session.commit()
    return 'OK'


@view.route('/api/v1.0/updateanswer', methods=['POST'])
def update_answer():
    post = request.get_json()
    id = post.get('id')
    answercorrect = post.get('correct')
    person_id = session['userid']
    sa = SubAnswerGiven.query.filter_by(id=id).first()
    sa.correct = answercorrect
    sa.person_id = person_id
    db.session.commit()
    return 'OK'


@view.route('/api/v1.0/reset', methods=['POST'])
def reset():
    SubAnswerGiven.query.delete()
    db.session.commit()
    return 'OK'


@view.route('/api/v1.0/newteam', methods=['POST'])
def addteam():
    post = request.get_json()
    teamname = post.get('teamname')
    team = Team(teamname=teamname)
    db.session.add(team)
    db.session.commit()
    return 'OK'


@view.route('/api/v1.0/removeteam', methods=['POST'])
def remove_team():
    post = request.get_json()
    id = post.get('id')
    Team.query.filter_by(id=id).delete()
    db.session.commit()
    return 'OK'


@view.route('/api/v1.0/removeteams', methods=['POST'])
def remove_teams():
    Team.query.delete()
    db.session.commit()
    return 'OK'


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
        return "answersheet is being processed"

