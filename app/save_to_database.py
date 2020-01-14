from view.models import Answersheet
from view.models import Team


def save_answersheet_database(db, answersheet):
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


def save_team_database(db, team_name):
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


def update_team_answersheet(db, answersheet_id, team_id):
    print("linking team %s with answersheet %s" % (team_id, answersheet_id))
    answersheet = Answersheet.query.filter_by(id=answersheet_id).first()
    if answersheet is None:
        print("this should not happen!")
        return False
    team = Team.query.filter_by(id=team_id).first()
    if team is None:
        print("this should not happen!")
        return False
    answersheet.set_team_id(team_id)
    db.session.add(answersheet)
    db.session.commit()
    return True

