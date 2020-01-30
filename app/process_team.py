import pytesseract
from view.models import Team
from fuzzywuzzy import fuzz, process
from app.save_to_database import save_team_database


def read_team(line):
    team_name_image = line
    team_name_image = team_name_image[:, 130:(len(team_name_image[0]))]
    team_name = pytesseract.image_to_string(team_name_image).replace("\n", " ")

    if "Naam:" in team_name:
        # We take the name of the team and remove leading whitespaces
        name_of_team = team_name.split("Naam:")[1]
        name_of_team = name_of_team.lstrip()

        name_of_team = check_team_name(name_of_team)

        team_id = save_team_database(name_of_team)
        print("the team name is: " + name_of_team)
        return team_id
    else:
        print("failed!")
        return None


def check_team_name(name_of_team):
    """
    We compare the given team with all the teams that are cooperating in the quiz.
    The team that has the most similarities will be the team that is chosen.
    This is because there can be a mistake with reading the team names
    """
    all_teams = Team.query.all()
    highest_ratio = 0
    team_result = name_of_team
    for t in all_teams:
        t_name = t.get_team_name()
        correct_ratio = fuzz.WRatio(name_of_team, t_name)
        if correct_ratio > highest_ratio:
            highest_ratio = correct_ratio
            team_result = t_name
    # If the team found completely matches a team in the db or if it's the first team it will return what as given.
    return team_result

