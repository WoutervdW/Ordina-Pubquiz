from view import view, db
from flask import jsonify, request
from sqlalchemy import func, inspect
from view.models import SubAnswerGiven, Team, TeamSchema, Word, Line, Answersheet, QuestionNumber, AnswerGiven

def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}

@view.route('/api/v1.0/teams', methods=['GET'])
def get_teams():
    results = db.session.query(Team, func.count(SubAnswerGiven.id) .label('score')).group_by(Team.id).filter(SubAnswerGiven.correct).filter(SubAnswerGiven.answergiven_id == AnswerGiven.id).filter(Team.id == AnswerGiven.team_id).all()
    teams = Team.query.all()
    teams_schema = TeamSchema(many=True)
    for i in range(0, len(results)):
        teamid = results[i][0].id
        team = Team.query.filter_by(id=teamid).first()
        team.score = results[i][1]
    result = teams_schema.dump(teams)
    return jsonify(result)


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


@view.route('/api/v1.0/nuke/all', methods=['POST'])
def nuke_all_button():
    SubAnswerGiven.query.delete()
    db.session.commit()
    db.engine.execute('alter sequence subanswergiven_id_seq RESTART with 1')

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


@view.route('/api/v1.0/updateteam', methods=['POST'])
def edit_team():
   post = request.get_json()
   id = post.get('id')
   teamname = post.get('teamname')
   team = Team.query.filter_by(id=id).first()
   team.teamname = teamname
   db.session.commit()
   return 'OK'

