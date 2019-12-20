from flask_testing import TestCase
from flask import Flask


class AnswerRouteTest(TestCase):

    def create_app(self):

        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

