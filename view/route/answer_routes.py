from answer_checking import answer_checker
from view import view, db
from flask import request, session, render_template, redirect, url_for
from view.models import SubAnswerGiven
import answer_checking.answer_checker
import threading


@view.route('/api/v1.0/updateanswer', methods=['POST'])
def update_answer():
    post = request.get_json()
    id = post.get('id')
    answercorrect = post.get('correct')
    person_id = session['userid']
    sa = SubAnswerGiven.query.filter_by(id=id).first()
    sa.correct = answercorrect
    print(answercorrect)
    sa.person_id = person_id
    db.session.commit()
    return 'OK'


@view.route('/api/v1.0/reset', methods=['POST'])
def reset():
    SubAnswerGiven.query.delete()
    db.session.commit()
    return 'OK'


@view.route('/api/v1.0/checkanswers', methods=['POST', 'GET'])
def check_answers():
    x = threading.Thread(target=answer_checker.check_all_answers)
    print("thread started")
    x.start()
    x.join()
    return render_template('answerchecking.html', checkinganswers=False)



