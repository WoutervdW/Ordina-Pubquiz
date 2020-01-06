from view import view, db
from flask import jsonify, request
from flask_cors import cross_origin
from sqlalchemy import func
from view.models import SubAnswerGiven, Team, TeamSchema


@cross_origin()
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