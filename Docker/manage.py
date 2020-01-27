import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from view.config import Config
from home import view, db

app = view
app.config.from_object(Config)
POSTGRES = {
    'user': os.environ.get('POSTGRES_USER'),
    'pw': os.environ.get('POSTGRES_PASSWORD'),
    'db': os.environ.get('POSTGRES_DATABASE'),
    'host': os.environ.get('POSTGRES_HOST'),
    'port': os.environ.get('POSTGRES_PORT')
}
app.config['SQLALCHEMY_DATABASE_URL'] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()

