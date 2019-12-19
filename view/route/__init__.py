from view.route.word_routes import word_all
from view.route.word_routes import load_word
from view.route.word_routes import nuke_all_words

from view.route.line_routes import lines_all
from view.route.line_routes import load_lines
from view.route.line_routes import nuke_all_lines
from view.route.line_routes import get_answersheets_lines

from view.route.answersheet_routes import answersheet_all
from view.route.answersheet_routes import load_answersheet
from view.route.answersheet_routes import nuke_all_answersheets


from view.route.answer_routes import update_answer
from view.route.answer_routes import reset
from view.route.answer_routes import check_answers

from view.route.question_routes import get_questions
from view.route.question_routes import get_categories
from view.route.question_routes import get_persons
from view.route.question_routes import get_answers
from view.route.question_routes import update_question
from view.route.question_routes import remove_question
from view.route.question_routes import add_question

from view.route.render_templates_routes import index
from view.route.render_templates_routes import questions
from view.route.render_templates_routes import answers
from view.route.render_templates_routes import uploadsheets
from view.route.render_templates_routes import reveal
from view.route.render_templates_routes import playquestions
from view.route.render_templates_routes import login
from view.route.render_templates_routes import logout
from view.route.render_templates_routes import do_login

from view.route.team_routes import get_teams
from view.route.team_routes import addteam
from view.route.team_routes import remove_team
from view.route.team_routes import remove_teams

from view.route.upload_routes import upload
