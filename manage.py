import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from view.config import Config
from home import view, db

app = view
# Insert the code from .flaskenv file here
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()

