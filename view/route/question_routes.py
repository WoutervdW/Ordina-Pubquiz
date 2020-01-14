from view import view, db
from flask import request, session, jsonify, url_for, flash
from view.models import Question, QuestionSchema, SubAnswer, Variant, Category, CategorySchema, Person, PersonSchema, SubAnswerGiven, SubAnswerGivenSchema


@view.route('/api/v1.0/questions', methods=['GET'])
def get_questions():
    questions_schema = QuestionSchema(many=True)
    allquestions = Question.query.all()
    result = questions_schema.dump(allquestions)
    return jsonify(result)


@view.route('/api/v1.0/categories', methods=['GET'])
def get_categories():
    categories_schema = CategorySchema(many=True)
    allcategories = Category.query.all()
    result = categories_schema.dump(allcategories)
    return jsonify(result)


@view.route('/api/v1.0/persons', methods=['GET'])
def get_persons():
    persons_schema = PersonSchema(many=True)
    people = Person.query.all()
    result = persons_schema.dump(people)
    return jsonify(result)


@view.route('/api/v1.0/subanswers', methods=['GET'])
def get_answers():
    answers_schema = SubAnswerGivenSchema(many=True)
    allanswers = SubAnswerGiven.query.all()
    result = answers_schema.dump(allanswers)
    return jsonify(result)


@view.route('/api/v1.0/updatequestion', methods=['POST'])
def update_question():
    post = request.get_json()
    id = post.get('id')
    q = Question.query.filter_by(id=id).first()
    if post.get('active') is not None:
        questionactive = post.get('active')
        q.active = questionactive
    if post.get('questionnumber').isdigit():
        questionnumber = int(post.get('questionnumber'))
        qtemp = Question.query.filter_by(questionnumber=questionnumber).first()
        if qtemp is None:
            q.questionnumber = questionnumber
        else:
            if qtemp.id != id:
                return 'De vraag kan niet worden aangepast. Er is al een vraag met dit nummer.'
            else:
                q.questionnumber = questionnumber
    else:
        q.questionnumber = None
    db.session.commit()
    return


@view.route('/api/v1.0/removequestion', methods=['POST'])
def remove_question():
    post = request.get_json()
    id = post.get('id')
    subanswers = SubAnswer.query.filter_by(question_id=id).all()
    for subanswer in subanswers:
        Variant.query.filter_by(subanswer_id=subanswer.id).delete()
    SubAnswer.query.filter_by(question_id=id).delete()
    Question.query.filter_by(id=id).delete()
    db.session.commit()
    return 'OK'


@view.route('/api/v1.0/newquestion', methods=['POST'])
def add_question():
    post = request.get_json()
    newquestionnumber = post.get('questionnumber')
    if newquestionnumber.isdigit():
        newquestionnumber = int(newquestionnumber)
        qtemp = Question.query.filter_by(questionnumber=newquestionnumber).first()
        if qtemp is not None:
            return 'De vraag kan niet worden toegevoegd. Er is al een vraag met dit nummer.'
    else:
        newquestionnumber = None
    newquestion = post.get('question')
    newsubanswers = post.get('subanswers')
    subanswers = []
    variants = []
    for i in range(0, len(newsubanswers)):
        for j in range(0, len(newsubanswers[i]['variants'])):
            variant = Variant(answer=newsubanswers[i]['variants'][j]['answer'])
            variants.append(variant);
        subanswer = SubAnswer(variants=variants)
        subanswers.append(subanswer)
        variants = []
    newquestioncategory = post.get('category')
    category = Category.query.filter(Category.name == newquestioncategory).first()
    print(category)
    if category is None:
        category = Category(name=newquestioncategory)

    newquestionperson_id = session['userid']
    newquestionactive = post.get('active')
    q = Question(questionnumber=newquestionnumber, question=newquestion, questioncategory=category,
        person_id=newquestionperson_id, active=newquestionactive, subanswers=subanswers)
    db.session.add(q)
    db.session.commit()
    return



