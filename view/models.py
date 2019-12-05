from view import db, ma
import json


class Team(db.Model):
    __tablename__ = 'team'
    id = db.Column(db.Integer, primary_key=True)
    teamname = db.Column(db.String(255))
    score = db.Column(db.Integer)

    def __init__(self, username, email):
        self.teamname = teamname
        self.score = score


class TeamSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('teamname', 'score')


class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    question = db.Column(db.String(255))
    correct_answer = db.Column(db.String(255))
    active = db.Column(db.Boolean)


class QuestionSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id', 'user_id', 'category_id', 'question', 'correct_answer', 'active')


class Answer(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable = False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    answer_given = db.Column(db.String(255))
    correct = db.Column(db.Boolean)
    confidence = db.Column(db.Float)
    answer_image = db.Column(db.LargeBinary)
    image_width = db.Column(db.Integer)
    image_height = db.Column(db.Integer)


class AnswerSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id', 'team_id', 'question_id', 'user_id', 'answer_given', 'correct', 'answer_image', 'confidence')


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))


class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id', 'username')


class Answersheet(db.Model):
    __tablename__ = 'answersheet'
    id = db.Column(db.Integer, primary_key=True)
    answersheet_image = db.Column(db.LargeBinary)
    image_width = db.Column(db.Integer)
    image_height = db.Column(db.Integer)


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class CategorySchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id', 'name')


class AnswerSheetQuestion(db.Model):
    __tablename__ = 'answersheetquestion'
    id = db.Column(db.Integer, primary_key=True)
    answersheet_id = db.Column(db.Integer, db.ForeignKey('answersheet.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))

