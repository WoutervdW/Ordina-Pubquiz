from flask_alchemydumps import AlchemyDumps, AlchemyDumpsCommand
from flask import Flask
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemyc

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

