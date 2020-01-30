from view.models import Answersheet
from view.models import Team
from view.models import QuestionNumber
from view import db


def save_answersheet_database(answersheet):
    print("saving answersheet to the database")
    # Save the image to the database!
    # convert the image to byte array so it can be saved in the database
    answer = answersheet.tostring()
    # create an Image object to store it in the database
    width = len(answersheet)
    height = len(answersheet[0])

    new_answersheet = Answersheet(
        answersheet_image=answer,
        image_width=width,
        image_height=height
    )
    # add the object to the database session
    db.session.add(new_answersheet)
    # commit the session so that the image is stored in the database
    db.session.commit()
    answersheet_id = new_answersheet.id
    return answersheet_id


def save_team_database(team_name):
    print("saving teamname to database")
    team = Team.query.filter_by(teamname=team_name).first()
    if team is None:
        # The team does not exist yet, so we will create it with 0 score.
        team = Team(
            teamname=team_name,
            score=0
        )
        db.session.add(team)
        db.session.commit()
        # return the team id so we can link it to the coming questions and answers
        return team.id
    else:
        # If the team exists we will return the id
        return team.id


def update_team_answersheet(answersheet_id, team_id):
    answersheet = Answersheet.query.filter_by(id=answersheet_id).first()
    if answersheet is None:
        print("failed!")
        return False
    team = Team.query.filter_by(id=team_id).first()
    if team is None:
        print("failed!")
        return False
    answersheet.set_team_id(team_id)
    db.session.add(answersheet)
    db.session.commit()
    return True


def save_question_number(question_image, question_number):
    q_image = question_image.tostring()

    question_width = len(question_image)
    question_height = len(question_image[0])

    question_recognized = QuestionNumber(
        question_number=question_number,
        question_image=q_image,
        image_width=question_width,
        image_height=question_height
    )
    # add the object to the database session
    db.session.add(question_recognized)
    # commit the session so that the image is stored in the database
    db.session.commit()

