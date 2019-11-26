from view import db

class Team(db.Model):
    __tablename__ = 'team'
    id = db.Column(db.Integer, primary_key=True)
    teamname = db.Column(db.String(255))
    score = db.Column(db.Integer)

class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    category_id = db.Column(db.String(255))
    question = db.Column(db.String(255))
    correct_answer = db.Column(db.String(255))
    active = db.Column(db.Boolean)

class Answer(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable = False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    correct = db.Column(db.Boolean)
    answer_image = db.Column(db.LargeBinary)
    confidence = db.Column(db.Float)

class User(db.Model):
    __tablename__= 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))

class Answersheet(db.Model):
    __tablename__ = 'answersheet'
    id = db.Column(db.Integer, primary_key=True)
    answersheet_image = db.Column(db.LargeBinary)

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255))

class AnswerSheetQuestion(db.Model):
    __tablename__ = 'answersheetquestion'
    id = db.Column(db.Integer, primary_key = True)
    answersheet_id = db.Column(db.Integer, db.ForeignKey('answersheet.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))







