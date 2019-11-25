from flask import Flask
from view.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap


view = Flask(__name__)
view.config.from_object(Config)

bootstrap = Bootstrap(view)

#db = SQLAlchemy(view)
#migrate = Migrate(view, db)

#from view import routes, models
from view import routes
