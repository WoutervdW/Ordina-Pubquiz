from view import view
from flask import render_template
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy

from view.models import Team
from view.models import TeamSchema


import psycopg2
from collections import OrderedDict


@view.route('/')
@view.route('/index')
def index():
    return render_template('index.html')


@view.route('/api/v1.0/teams', methods=['GET'])
def get_teams():
    teams_schema = TeamSchema(many=True)
    teams = Team.query.all()
    result = teams_schema.dump(teams)
    return jsonify(result);

