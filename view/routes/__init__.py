from view.routes.word_routes import word_all
from view.routes.word_routes import load_word
from view.routes.word_routes import nuke_all_words

from view.routes.line_routes import lines_all
from view.routes.line_routes import load_lines
from view.routes.line_routes import nuke_all_lines
from view.routes.line_routes import get_answersheets_lines

from view.routes.answersheet_routes import answersheet_all
from view.routes.answersheet_routes import load_answersheet
from view.routes.answersheet_routes import nuke_all_answersheets
from view.routes.answersheet_routes import nuke_all

from view.routes.answer_routes import update_answer
from view.routes.answer_routes import reset
from view.routes.answer_routes import check_answers

from view.routes.question_routes import get_questions
from view.routes.question_routes import get_categories
from view.routes.question_routes import get_persons
from view.routes.question_routes import get_answers
from view.routes.question_routes import update_question
from view.routes.question_routes import remove_question
from view.routes.question_routes import add_question

from view.routes.render_templates_routes import index
from view.routes.render_templates_routes import questions
from view.routes.render_templates_routes import answers
from view.routes.render_templates_routes import uploadsheets
from view.routes.render_templates_routes import reveal
from view.routes.render_templates_routes import playquestions
from view.routes.render_templates_routes import login
from view.routes.render_templates_routes import logout
from view.routes.render_templates_routes import do_login

from view.routes.team_routes import get_teams
from view.routes.team_routes import addteam
from view.routes.team_routes import remove_team
from view.routes.team_routes import remove_teams
from view.routes.team_routes import nuke_all_button

from view.routes.upload_routes import upload

from view.routes.question_number_routes import questions_all
from view.routes.question_number_routes import load_questions
from view.routes.question_number_routes import load_question_id
from view.routes.question_number_routes import nuke_all_questions
