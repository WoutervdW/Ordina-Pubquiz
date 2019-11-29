from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_marshmallow import Marshmallow
from flask import Flask
from view.config import Config


view = Flask(__name__)
view.config.from_object(Config)

bootstrap = Bootstrap(view)

db = SQLAlchemy(view)
ma = Marshmallow(view)

migrate = Migrate(view, db)

from view import routes, models

