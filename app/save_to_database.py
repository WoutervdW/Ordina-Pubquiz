from view.models import Answersheet
from view.models import Team
from view.models import QuestionNumber
from view.models import Line
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
    print("read the team name %s" % team.get_team_name())
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


def update_line_in_database(line_image, line_id):
    # This should always give a line back since it's the id we saved from saving it in the database a few moments ago
    line = Line.query.filter_by(id=line_id).first()

    if line is None:
        print("failed to update line!")
        return False

    print("begin saving line %s to the database with new image" % line_id)
    line_img = line_image.tostring()
    print("line_iamge information %s" % (len(line_img)))
    # create an Image object to store it in the database
    width = len(line_image)
    height = len(line_image[0])

    print("new line has width %s and height %s" % (width, height))

    line.line_image = line_img
    line.image_width = width
    line.image_height = height

    # commit the session so that the image is stored in the database
    db.session.commit()

    print("update line with id %s" % line_id)


def remove_line_in_database(line_id):
    # This should always give a line back since it's the id we saved from saving it in the database a few moments ago
    Line.query.filter_by(id=line_id).delete()
    # This line is not needed for anything, so we will remove it.
    db.session.commit()

