from view import view
from flask import render_template, session, request, redirect, flash, url_for
from view.models import Person, SubAnswerGiven


@view.route('/')
@view.route('/index')
def index():
    return render_template('index.html')


@view.route('/questions')
def questions():
    return render_template('questions.html')


@view.route('/answerchecking')
def answers():
    page = request.args.get('page', 1, type=int)
    answers = SubAnswerGiven.query.paginate(page, view.config['ANSWERS_PER_PAGE'], False)
    return render_template('answerchecking.html', subanswers=answers)


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