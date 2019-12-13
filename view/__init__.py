from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_bootstrap import Bootstrap
from flask_marshmallow import Marshmallow
from flask import Flask
from flask_login import LoginManager
from view.config import Config


view = Flask(__name__)
view.config.from_object(Config)
view.secret_key = 'some secret key that we will come up with'

bootstrap = Bootstrap(view)

db = SQLAlchemy(view)
ma = Marshmallow(view)

migrate = Migrate(view, db)
login = LoginManager(view)

from view import routes, models

