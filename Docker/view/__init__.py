from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_bootstrap import Bootstrap
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask import Flask
from view.config import Config


view = Flask(__name__)
view.config.from_object(Config)
view.secret_key = 'some secret key that we will come up with'
CORS(view, resources={r"/api/*": {"origins": "*"}})

bootstrap = Bootstrap(view)

db = SQLAlchemy(view)
ma = Marshmallow(view)

migrate = Migrate(view, db)

from view import routes, models

