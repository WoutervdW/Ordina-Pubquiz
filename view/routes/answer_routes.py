from answer_checking import answer_checker
from view import view, db
from flask import request, session, render_template, redirect, url_for, jsonify
from view.models import AnswerGiven, SubAnswerGiven, Word, Line, Answersheet, QuestionNumber, Person, PersonSchema
import answer_checking.answer_checker
import threading


@view.route('/api/v1.0/updateanswer', methods=['POST'])
def update_answer():
    post = request.get_json()
    id = post.get('id')
    answercorrect = post.get('correct')
    person = Person.query.filter_by(personname='admin').first()
    sa = SubAnswerGiven.query.filter_by(id=id).first()
    sa.correct = answercorrect
    sa.person_id = person.id
    print("PERSON", person)
    db.session.commit()
    person_schema = PersonSchema()
    result = person_schema.dump(person)
    return jsonify(result)


@view.route('/api/v1.0/reset', methods=['POST'])
def reset():
    SubAnswerGiven.query.delete()
    db.session.commit()
    db.engine.execute('alter sequence subanswergiven_id_seq RESTART with 1')

    AnswerGiven.query.delete()
    db.session.commit()
    db.engine.execute('alter sequence answergiven_id_seq RESTART with 1')

    Word.query.delete()
    db.session.commit()
    db.engine.execute('alter sequence word_id_seq RESTART with 1')

    Line.query.delete()
    db.session.commit()
    db.engine.execute('alter sequence line_id_seq RESTART with 1')

    Answersheet.query.delete()
    db.session.commit()
    db.engine.execute('alter sequence answersheet_id_seq RESTART with 1')

    QuestionNumber.query.delete()
    db.session.commit()
    db.engine.execute('alter sequence questionnumber_id_seq RESTART with 1')

    return 'OK'


@view.route('/api/v1.0/checkanswers', methods=['POST', 'GET'])
def check_answers():
    x = threading.Thread(target=answer_checker.iterate_questions)
    print("thread started")
    x.start()
    x.join()
    return render_template('answerchecking.html', checkinganswers=False)



