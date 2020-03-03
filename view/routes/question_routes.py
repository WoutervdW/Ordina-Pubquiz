from view import view, db
from flask import request, session, jsonify, url_for, flash
from view.models import Question, QuestionSchema, SubAnswer, Variant, Category, CategorySchema, Person, PersonSchema, AnswerGiven, AnswerGivenSchema, SubAnswerGiven, Team
from view.config import Config
from flask import render_template


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


@view.route('/api/v1.0/category/<string:name>', methods=['GET'])
def get_category(name):
    categories_schema = CategorySchema()
    category = Category.query.filter_by(name=name).first()
    result = categories_schema.dump(category)
    return jsonify(result)


@view.route('/api/v1.0/persons', methods=['GET'])
def get_persons():
    persons_schema = PersonSchema(many=True)
    people = Person.query.all()
    result = persons_schema.dump(people)
    return jsonify(result)


@view.route('/api/v1.0/answers', methods=['GET'])
def get_answers():
    answers_schema = AnswerGivenSchema(many=True)
    question_id = request.args.get('question_id', 0, type=int)
    team_id = request.args.get('team_id', 0, type=int)
    correct = request.args.get('correct', None, type=bool)
    category_id = request.args.get('category_id', 0, type=int)
    # checked_by is the person_id
    person_id = request.args.get('checkedby_id', 0, type=int)
    confidence_from = request.args.get('confidence_from', None, type=int)
    confidence_to = request.args.get('confidence_to', None, type=int)
    # Wow this is a mess! The others are filtered by things separate! Even though it will load a lot more,
    # it will be a lot less than loading everything
    # This filters 'category', 'question', 'person' and 'team' or any combination of these.
    if category_id != 0:
        if question_id == 0 \
                and team_id == 0 \
                and person_id == 0:
            questions = Question.query.filter_by(category_id=category_id).all()
            question_ids = []
            for q in questions:
                question_ids.append(q.id)
            allanswers = AnswerGiven.query.filter(AnswerGiven.question_id.in_((question_ids)))
        elif question_id != 0 \
                and team_id == 0 \
                and person_id == 0:
            questions = Question.query.filter_by(category_id=category_id, id=question_id).all()
            question_ids = []
            for q in questions:
                question_ids.append(q.id)
            allanswers = AnswerGiven.query.filter(AnswerGiven.question_id.in_((question_ids)))
        elif question_id == 0 \
                and team_id != 0 \
                and person_id == 0:
            questions = Question.query.filter_by(category_id=category_id).all()
            question_ids = []
            for q in questions:
                question_ids.append(q.id)
            allanswers = AnswerGiven.query.filter(AnswerGiven.question_id.in_((question_ids))).filter_by(team_id=team_id)
        elif question_id != 0 \
                and team_id != 0 \
                and person_id == 0:
            questions = Question.query.filter_by(category_id=category_id, id=question_id).all()
            question_ids = []
            for q in questions:
                question_ids.append(q.id)
            allanswers = AnswerGiven.query.filter(AnswerGiven.question_id.in_((question_ids)))\
                .filter_by(team_id=team_id, question_id=question_id)
        elif question_id == 0 \
                and team_id == 0 \
                and person_id != 0:
            questions = Question.query.filter_by(category_id=category_id).all()
            question_ids = []
            for q in questions:
                question_ids.append(q.id)
            sub_answer_given = SubAnswerGiven.query.filter_by(person_id=person_id).all()
            ids = []
            for q in sub_answer_given:
                ids.append(q.answergiven_id)
            allanswers = AnswerGiven.query.filter(AnswerGiven.id.in_((ids))).filter(AnswerGiven.question_id.in_((question_ids)))
        elif question_id == 0 \
                and team_id != 0 \
                and person_id != 0:
            questions = Question.query.filter_by(category_id=category_id).all()
            question_ids = []
            for q in questions:
                question_ids.append(q.id)
            sub_answer_given = SubAnswerGiven.query.filter_by(person_id=person_id).all()
            ids = []
            for q in sub_answer_given:
                ids.append(q.answergiven_id)
            allanswers = AnswerGiven.query.filter(AnswerGiven.id.in_((ids))).filter(AnswerGiven.question_id.in_((question_ids))).filter_by(team_id=team_id)
        elif question_id != 0 \
                and team_id == 0 \
                and person_id != 0:
            questions = Question.query.filter_by(category_id=category_id, id=question_id).all()
            question_ids = []
            for q in questions:
                question_ids.append(q.id)
            sub_answer_given = SubAnswerGiven.query.filter_by(person_id=person_id).all()
            ids = []
            for q in sub_answer_given:
                ids.append(q.answergiven_id)
            allanswers = AnswerGiven.query.filter(AnswerGiven.id.in_((ids))).filter(AnswerGiven.question_id.in_((question_ids)))
        elif question_id != 0 \
                and team_id != 0 \
                and person_id != 0:
            questions = Question.query.filter_by(category_id=category_id, id=question_id).all()
            question_ids = []
            for q in questions:
                question_ids.append(q.id)
            sub_answer_given = SubAnswerGiven.query.filter_by(person_id=person_id).all()
            ids = []
            for q in sub_answer_given:
                ids.append(q.answergiven_id)
            allanswers = AnswerGiven.query.filter(AnswerGiven.id.in_((ids))).filter(
                AnswerGiven.question_id.in_((question_ids))).filter_by(team_id=team_id)
    else:
        if question_id != 0 \
                and team_id == 0 \
                and person_id == 0:
            allanswers = AnswerGiven.query.filter_by(question_id=question_id)
        elif question_id == 0 \
                and team_id != 0 \
                and person_id == 0:
            allanswers = AnswerGiven.query.filter_by(team_id=team_id)
        elif question_id != 0 \
                and team_id != 0 \
                and person_id == 0:
            allanswers = AnswerGiven.query.filter_by(question_id=question_id, team_id=team_id)
        elif question_id == 0 \
                and team_id == 0 \
                and person_id != 0:
            sub_answer_given = SubAnswerGiven.query.filter_by(person_id=person_id).all()
            ids = []
            for q in sub_answer_given:
                ids.append(q.answergiven_id)
            allanswers = AnswerGiven.query.filter(AnswerGiven.id.in_((ids)))
        elif question_id == 0 \
                and team_id != 0 \
                and person_id != 0:
            sub_answer_given = SubAnswerGiven.query.filter_by(person_id=person_id).all()
            ids = []
            for q in sub_answer_given:
                ids.append(q.answergiven_id)
            allanswers = AnswerGiven.query.filter(AnswerGiven.id.in_((ids))).filter_by(team_id=team_id)
        elif question_id != 0 \
                and team_id == 0 \
                and person_id != 0:
            sub_answer_given = SubAnswerGiven.query.filter_by(person_id=person_id).all()
            ids = []
            for q in sub_answer_given:
                ids.append(q.answergiven_id)
            allanswers = AnswerGiven.query.filter(AnswerGiven.id.in_((ids))).filter_by(question_id=question_id)
        elif question_id != 0 \
                and team_id != 0 \
                and person_id != 0:
            sub_answer_given = SubAnswerGiven.query.filter_by(person_id=person_id).all()
            ids = []
            for q in sub_answer_given:
                ids.append(q.answergiven_id)
            allanswers = AnswerGiven.query.filter(AnswerGiven.id.in_((ids))).filter_by(team_id=team_id, question_id=question_id)
        else:
            print("something went wrong")
            allanswers = AnswerGiven.query.all()

    # This filters 'confidence_from' and 'confidence_to'
    # After the initial filtering we filter out the confidence and later the correct.
    if confidence_to is not None:
        # We set the confidence_from to 0 if nothing is filled, because it seems logical from a user perspective.
        if confidence_from is None:
            confidence_from = 0
        answersgiven_ids = []
        for item in allanswers:
            answer_given = AnswerGiven.query.filter_by(id=item.id).first()
            if answer_given is not None:
                sub_answer_givens = answer_given.subanswersgiven
                for sub_answer_given in sub_answer_givens:
                    confidence = sub_answer_given.confidence
                    # We now filter out any confidences that we don't want to show.
                    if confidence <= confidence_to:
                        # The confidence is below 'confidence_to'. When also above 'confidence_from' We will show it.
                        if confidence >= confidence_from:
                            if item.id not in answersgiven_ids:
                                answersgiven_ids.append(item.id)
        allanswers = AnswerGiven.query.filter(AnswerGiven.id.in_((answersgiven_ids)))

    # This filters a special case of 'confidence_from' and 'confidence_to'
    if confidence_to is None and confidence_from is not None:
        # If the user only gave a confidence_from we only filter out those values
        answersgiven_ids = []
        for item in allanswers:
            answer_given = AnswerGiven.query.filter_by(id=item.id).first()
            if answer_given is not None:
                sub_answer_givens = answer_given.subanswersgiven
                for sub_answer_given in sub_answer_givens:
                    confidence = sub_answer_given.confidence
                    # We now filter out any confidences that we don't want to show.
                    if confidence >= confidence_from:
                        if item.id not in answersgiven_ids:
                            answersgiven_ids.append(item.id)
        allanswers = AnswerGiven.query.filter(AnswerGiven.id.in_((answersgiven_ids)))

    # This filters the 'correct'
    if correct is not None:
        answersgiven_ids = []
        for item in allanswers:
            answer_given = AnswerGiven.query.filter_by(id=item.id).first()
            if answer_given is not None:
                sub_answer_givens = answer_given.subanswersgiven
                for sub_answer_given in sub_answer_givens:
                    answer_correct = sub_answer_given.correct
                    if answer_correct == correct:
                        if item.id not in answersgiven_ids:
                            answersgiven_ids.append(item.id)
        allanswers = AnswerGiven.query.filter(AnswerGiven.id.in_((answersgiven_ids)))

    if question_id == 0 and team_id == 0 and correct is None and category_id == 0 and person_id == 0 and confidence_from is None and confidence_to is None:
        # If none of the filters are given, we set a default filtering, which I'll set to a question
           allanswers = AnswerGiven.query.paginate(1, 100, False).items

    result = answers_schema.dump(allanswers)
    return jsonify(result)


@view.route('/api/v1.0/updatequestion', methods=['POST'])
def update_question():
    post = request.get_json()
    id = post.get('id')
    q = Question.query.filter_by(id=id).first()
    if str(post.get('questionnumber')).isdigit():
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
        return 'De vraag kan niet worden aangepast. Er is geen geldig vraagnummer ingevoerd'

    q.question = post.get('question')
    newsubanswers = post.get('subanswers')
    variants = []
    subanswers=[]
    for i in range(0, len(newsubanswers)):
        for j in range(0, len(newsubanswers[i]['variants'])):
            variant = Variant(answer=newsubanswers[i]['variants'][j]['answer'])
            variants.append(variant);
        subanswer = SubAnswer(variants=variants)
        subanswers.append(subanswer)
        variants = []
    q.subanswers = subanswers
    newcategory = post.get('category')
    category = Category.query.filter(Category.name == newcategory).first()
    if category is None:
        category = Category(name=newcategory)
    q.questioncategory = category
    db.session.commit()
    return 'OK'


@view.route('/api/v1.0/removequestion', methods=['POST'])
def remove_question():
    post = request.get_json()
    id = post.get('id')
    subanswers = SubAnswer.query.filter_by(question_id=id).all()
    try:
        for subanswer in subanswers:
            Variant.query.filter_by(subanswer_id=subanswer.id).delete()
        SubAnswer.query.filter_by(question_id=id).delete()
        Question.query.filter_by(id=id).delete()
        db.session.commit()
    except:
        return 'Vraag kan niet verwijderd worden. Er zijn nog antwoorden gekoppeld aan deze vraag'
    return 'OK'


@view.route('/api/v1.0/newquestion', methods=['POST'])
def add_question():
    post = request.get_json()
    newquestionnumber = post.get('questionnumber')
    if newquestionnumber.isdigit():
        newquestionnumber = int(newquestionnumber)
        qtemp = Question.query.filter_by(questionnumber=newquestionnumber).first()
        if qtemp is not None:
            return 'Fout: De vraag kan niet worden toegevoegd. Er is al een vraag met dit nummer.'
    else:
        return 'Fout: De vraag kan niet worden toegevoegd. Er is geen geldig vraagnummer ingevoerd'
    newquestion = post.get('question')
    newsubanswers = post.get('subanswers')
    subanswers = []
    variants = []
    for i in range(0, len(newsubanswers)):
        for j in range(0, len(newsubanswers[i]['variants'])):
            variant = Variant(answer=newsubanswers[i]['variants'][j]['answer'])
            variants.append(variant)
        subanswer = SubAnswer(variants=variants)
        subanswers.append(subanswer)
        variants = []
    newquestioncategory = post.get('category')
    category = Category.query.filter(Category.name == newquestioncategory).first()
    if category is None:
        category = Category(name=newquestioncategory)
    newquestionperson_id = session['userid']
    newquestionactive = post.get('active')
    q = Question(questionnumber=newquestionnumber, question=newquestion, questioncategory=category,
        person_id=newquestionperson_id, active=newquestionactive, subanswers=subanswers)
    db.session.add(q)
    db.session.commit()
    question_schema = QuestionSchema()
    result = question_schema.dump(q)
    return jsonify(result)


@view.route('/api/v1.0/resetquestionnumbers', methods=['POST'])
def resetnumbers():
    questions = Question.query.all()
    for question in questions:
        question.questionnumber = None
    db.session.commit()
    return 'OK'


@view.route('/api/v1.0/deleteallquestions', methods=['POST'])
def deletequestions():
    try:
        Variant.query.delete()
        db.engine.execute('alter sequence variant_id_seq RESTART with 1')
        SubAnswer.query.delete()
        db.engine.execute('alter sequence subanswer_id_seq RESTART with 1')
        Question.query.delete()
        db.engine.execute('alter sequence question_id_seq RESTART with 1')
        db.session.commit()
    except:
        return 'Vragen kunnen niet verwijderd worden. Er zijn nog antwoorden gekoppeld aan tenminste een vraag'
    return 'OK'


@view.route('/api/v1.0/removecategory', methods=['POST'])
def remove_category():
    post = request.get_json()
    id = post.get('id')
    try:
        Category.query.filter_by(id=id).delete()
        db.session.commit()
    except:
        return 'Categorie kan niet verwijderd worden. Er zijn nog vragen gekoppeld aan deze categorie'
    return 'OK'

