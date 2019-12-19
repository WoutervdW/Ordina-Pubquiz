from view import view, db
from flask import request, session
from view.models import SubAnswerGiven
import answer_checking


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


@view.route('/api/v1.p/checkanswers', methods=['POST'])
def check_answers():
    answer_checking.check_all_answers(db)
    return "answers are checked"
