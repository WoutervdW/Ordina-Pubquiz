from view import view
from flask import render_template
from view.models import Team

import psycopg2


@view.route('/')
@view.route('/index')
def index():
    teams = Team.query.all()
    return render_template('index.html', teams=teams)
    #connection = psycopg2.connect(user="mot23897",
    ##                              password="admin",
    #                              host="127.0.0.1",
    #                              port="5432",
    #                              database="mot23897")
    #cursor=connection.cursor()
    #query_selectteams = "select * from team"
    #cursor.execute(query_selectteams)
    #teams = cursor.fetchall()
    #connection.close()

