from alchemydumps import AlchemyDumps, AlchemyDumpsCommand
from flask import Flask
from flask.ext.script import Manager
from flask.ext.sqlalchemy import SQLAlchemy

# init Flask
app = Flask(__name__)

# init SQLAlchemy and Flask-Script
POSTGRES = {
}
# app.config['SQLALCHEMY_DATABASE_URL'] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
db = SQLAlchemy(app)
manager = Manager(app)


# init Alchemy Dumps
alchemydumps = AlchemyDumps(app, db)
manager.add_command('alchemydumps', AlchemyDumpsCommand)

