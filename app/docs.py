import math
from view import db
from docx import Document
from docx.shared import Cm, Mm, Pt
from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT
from view.models import Question, Team, SubAnswer
from sqlalchemy import func
from datetime import datetime

answers_per_page = 13
column_width_number = Mm(22.8)
column_width_answer = Mm(162.2)
row_height = Mm(19)
margin = Mm(12.7)
page_width = Mm(210)
page_height = Mm(297)
document = None


def create_doc(post):
    document = Document()
    breaks = []
    for p in post:
        breaks.append(p)
    lines = calculate_lines()
    sections = document.sections
    for section in sections:
        section.top_margin = margin
        section.bottom_margin = margin
        section.left_margin = margin
        section.right_margin = margin
        section.page_width = page_width
        section.page_height = page_height

    style = document.styles['Normal']
    font = style.font
    font.name = 'Calibri'
    font.size = Pt(22)
    teams = Team.query.all()
    print("ALLE TEAMS", teams)
    for team in teams:
        print("VOEG TOE TEAM", team)
        add_team(lines, team, breaks)
    try:
        document.save(getFileName())
        return 'Document is opgeslagen'
    except:
        return 'Er is iets fout gegaan bij het opslaan van het bestand. Probeer het opnieuw.'


def calculate_lines():
    amount = 0
    questions = Question.query.all()
    for question in questions:
        if question.questionnumber is not None:
            subanswers = question.subanswers
            for subanswer in subanswers:
                amount = amount + 1
    return amount


def add_team(lines, team, breaks):
    teamname = team.teamname
    pages = math.ceil(lines / answers_per_page)
    fromquestion = 1
    subanswersfromquestion = 0
    roundnumber = 0
    print("AANTAL PAGINAS:", pages)
    while True:
        print("NIEUWE PAGINA VOOR TEAM", teamname, "VANAF VRAAG", fromquestion)
        fromquestion, subanswersfromquestion, roundnumber, lastQ = add_page_for_team(teamname, fromquestion, subanswersfromquestion, roundnumber, breaks)
        if lastQ:
            break


def add_page_for_team(teamname, fromquestion, subanswersfromquestion, roundnumber, breaks):
    table = document.add_table(rows=answers_per_page+1, cols=2)
    table.style = 'TableGrid'
    table.rows[0].height = row_height
    title = table.rows[0].cells
    title[0].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    title[1].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    title[0].width = column_width_number
    title[1].width = column_width_answer
    title[0].text = 'Quiz'
    title[1].text = 'Naam: ' + teamname
    rowsfilled = 0
    title[0].paragraphs[0].paragraph_format.alignment = WD_TABLE_ALIGNMENT.CENTER
    lastQForTeam = False
    lastQForBreak = False
    while rowsfilled < answers_per_page:
        currentrow = table.rows[rowsfilled + 1]
        currentrow.height = row_height
        currentrow.cells[0].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        currentrow.cells[1].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        currentrow.cells[0].width = column_width_number
        currentrow.cells[1].width = column_width_answer
        if lastQForTeam or lastQForBreak:
            rowsfilled = rowsfilled + 1
            continue
        q = Question.query.filter_by(questionnumber=fromquestion).first()
        if q is not None:
            s = db.session.query(func.count(SubAnswer.id)).group_by(SubAnswer.question_id).filter_by(question_id=q.id).all()
            subcount = s[0][0]
            if subcount > subanswersfromquestion:
                if isNewCategory(q, table.rows[rowsfilled]):
                    roundnumber += 1
                    currentrow.cells[0].text = ""
                    currentrow.cells[1].text = "Ronde " + str(roundnumber) + ": " + str(getCategoryNumber(q))
                    print("NIEUWE RONDE:", roundnumber)
                else:
                    currentrow.cells[0].text = str(q.questionnumber)
                    currentrow.cells[1].text = ""
                    subanswersfromquestion = subanswersfromquestion + 1
                    print("ZELFDE VRAAG", q.questionnumber)
                currentrow.cells[0].paragraphs[0].paragraph_format.alignment = WD_TABLE_ALIGNMENT.CENTER
                currentrow.cells[1].paragraphs[0].paragraph_format.alignment = WD_TABLE_ALIGNMENT.CENTER
                rowsfilled = rowsfilled + 1
            else:
                print("NIEUWE VRAAG")
                subanswersfromquestion = 0
                fromquestion = fromquestion + 1
        if isLastQuestion(q, subanswersfromquestion):
            print("LAATSTE")
            lastQForTeam = True
        if isBreak(q, subanswersfromquestion, breaks):
            lastQForBreak = True
    return q.questionnumber, subanswersfromquestion, roundnumber, lastQForTeam


def getFileName():
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d")
    filename = "pubquiz" + dt_string + ".docx"
    index = 1
    while True:
        try:
            open(filename, 'rb')
            filename = "pubquiz" + dt_string + "_" + str(index) + ".docx"
            index += 1
        except:
            return filename
    return


def isNewCategory(question, previousrow):
    if str(question.questionnumber) != str(previousrow.cells[0].text) and (previousrow.cells[0].text != "" or previousrow.cells[0].text == "Quiz"):
        currentCat = question.category_id
        previousQ = Question.query.filter_by(questionnumber=question.questionnumber - 1).first()
        if previousQ:
            previousCat = previousQ.category_id
            if previousCat != currentCat:
                return True
        else:
            return True
    return False


def getCategoryNumber(question):
    return question.questioncategory.name


def isLastQuestion(question, subanswersfromquestion):
    lastQ = Question.query.filter(Question.questionnumber>0).order_by(Question.questionnumber.desc()).first()
    if lastQ.questionnumber == question.questionnumber:
        amountOfSubanswers = db.session.query(func.count(SubAnswer.id)).filter_by(question_id=question.id).all()
        if amountOfSubanswers[0][0] == subanswersfromquestion:
            return True
    return False


def isBreak(question, subanswersfromquestion, breaks):
    if str(question.questionnumber) in breaks:
        print("VRAAGNUMMER", question.questionnumber)
        amountOfSubanswers = db.session.query(func.count(SubAnswer.id)).filter_by(question_id=question.id).all()
        print("BIJ", subanswersfromquestion, "ER ZIJN ER ", amountOfSubanswers[0][0])
        if amountOfSubanswers[0][0] == subanswersfromquestion:
            return True
    return False