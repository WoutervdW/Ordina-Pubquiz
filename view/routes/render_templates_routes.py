from view import view
from flask import render_template, session, request, redirect, flash, url_for
from view.models import Person, SubAnswerGiven
from view.config import Config


@view.route('/')
@view.route('/index')
def index():
    return render_template('index.html')


@view.route('/questions')
def questions():
    return render_template('questions.html')


@view.route('/answerchecking')
def answers():
    vraag = request.args.get('vraag', 0, type=int)
    Config.vraag = vraag
    team = request.args.get('team', 0, type=int)
    Config.team = team
    categorie = request.args.get('categorie', 0, type=int)
    Config.categorie = categorie
    correct = request.args.get('correct', 0, type=int)
    Config.correct = correct
    nagekeken_door = request.args.get('nagekeken_door', 0, type=int)
    Config.nagekeken_door = nagekeken_door
    zekerheid_van = request.args.get('zekerheid_van', 0, type=int)
    Config.zekerheid_van = zekerheid_van
    zekerheid_tot = request.args.get('zekerheid_tot', 0, type=int)
    Config.zekerheid_tot = zekerheid_tot
    if 'message' in request.args:
        message = request.args['message']
        return render_template('answerchecking.html', message=message)
    return render_template('answerchecking.html')


@view.route('/uploadsheets')
def uploadsheets():
    return render_template('uploadsheets.html')


@view.route('/revealwinner')
def reveal():
    return render_template('revealwinner.html')


@view.route('/questionplayer')
def playquestions():
    return render_template('questionplayer.html')


@view.route('/login')
def login():
    if 'logged_in' in session and session['logged_in']:
        return render_template('index.html')
    return render_template('login.html')


@view.route("/logout")
def logout():
    session['logged_in'] = False
    return login()


@view.route('/api/v1.0/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    user = Person.query.filter_by(personname=username).first()
    if user:
        session['logged_in'] = True
        session['userid'] = user.id
        return redirect(url_for('index'))
    else:
        if user:
            flash('Wachtwoord klopt niet')
        else:
            flash('Gebruiker bestaat niet')
        return login()