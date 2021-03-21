import os
import babel
#from forms import *
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS


from models import db_drop_and_create_all, setup_db, Drink, Course, Player, Score
from auth import AuthError, requires_auth, JWTError

app = Flask(__name__)
setup_db(app)
CORS(app)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization,true'
                        )
    response.headers.add('Access-Control-Allow-Methods', 
                         'GET,POST,DELETE,PACTH,OPTIONS'
                        )
    return response

def paginate(request, selection):
    display_per_page = 10
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * display_per_page
    end = start + display_per_page
    paginated_data = selection[start:end]
    #questions = [question.format() for question in selection]
    #current_questions = questions[start:end]

    return paginated_data

@app.route('/players')
def retrieve_players():
    players = []
    player_query = Player.query.order_by(Player.id).all()
    pagenated_player_query = paginate(request, player_query)
    for player in pagenated_player_query:
        players.append([player.name, player.best_score])
        print(player.name, player.best_score)
    if len(players) == 0:
        abort(404)
    return jsonify({'success': True,
                    'players': players,
                    }), 200

@app.route('/players', methods=['POST'])
def create_player():
    body = request.get_json()
    new_name = body.get('name', None)
    new_image_link = body.get('image_link', None)
    new_seeking_course = body.get('seeking_course', None)
    new_seeking_description = body.get('seeking_description', None)
    new_best_score = body.get('best_score', None)
    print(new_name, new_best_score)
    try:
        player = Player(name=new_name,
                        image_link=new_image_link, 
                        seeking_course=new_seeking_course,
                        seeking_description=new_seeking_description,
                        best_score=new_best_score)
        player.insert()
        added_id = Player.query.filter(
                Player.name == new_name).one_or_none().format().get('id')
        print(added_id)
        return jsonify({'added_name': new_name})

    except BaseException:
        abort(422)

@app.route('/courses')
def retrieve_courses():
    courses = []
    course_query = Course.query.order_by(Course.id).all()
    for course in course_query:
        courses.append(course.name)
        print(course.name)
    if len(courses) == 0:
        abort(404)
    return jsonify({'success': True,
                    'courses': courses,
                    }), 200

@app.route('/courses', methods=['POST'])
@requires_auth('post:course')
def create_courses(payload):
    print(payload.get('sub'))
    body = request.get_json()
    new_name = body.get('name', None)
    new_state = body.get('state', None)
    new_image_link = body.get('image_link', None)
    print(new_name, new_state)
    try:
        course = Course(name=new_name,
                        state=new_state,
                        image_link=new_image_link)
        course.insert()
        added_id = Course.query.filter(
                Course.name == new_name).one_or_none().format().get('id')
        print(added_id)
        return jsonify({'added_name': new_name})

    except BaseException:
        abort(422)

@app.route('/scores')
def retrieve_scores():
    scores = []
    score_query = Score.query.order_by(Score.score).all()
    for score in score_query:
        scores.append(score.score)
        print(score.score)
    if len(scores) == 0:
        abort(404)
    return jsonify({'success': True,
                    'scores': scores,
                    }), 200

@app.route('/scores', methods=['POST'])
def create_scores():
    body = request.get_json()
    new_player_id = body.get('player_id', None)
    new_course_id = body.get('course_id', None)
    new_score = body.get('score', None)
    new_date = body.get('date', None)
    print(new_player_id, new_course_id, new_score)
    try:
        score = Score(player_id=new_player_id,
                        course_id=new_course_id,
                        score=new_score,
                        date=new_date)
        score.insert()
        return jsonify({'added_score': new_score})

    except BaseException:
        abort(422)

@app.route('/scores/<int:score_id>', methods=['DELETE'])
def delete_score(score_id):
    score = Score.query.filter(
        Score.id == score_id).one_or_none()
    if score is None:
        abort(404)

    score.delete()

    return jsonify({'deleted_id': score_id})

@app.route('/scores/<int:score_id>', methods=['PATCH'])
#@requires_auth('patch:drinks')
def update_score(score_id):
    score = Score.query.filter(Score.id == score_id).one_or_none()
    if score is None:
        abort(404)
    body = request.get_json()
    update_course_id = body.get('course_id', None)
    update_score = body.get('score', None)
    update_date = body.get('date', None)
    try:
        score.course_id = update_course_id
        score.score = update_score
        score.date = update_date
        score.update()
        return jsonify({'success': True,
                        'update coure_id, score, data': [update_course_id, update_score, update_date],
                        }), 200
    except BaseException:
        abort(422)



@app.route('/drinks')
def retrieve_drinks():
    drinks = []
    drink_query = Drink.query.order_by(Drink.id).all()
    for drink in drink_query:
        drinks.append(drink.recipe)#(drink.short())
        print(drink.recipe)
    if len(drinks) == 0:
        abort(404)
    return jsonify({'success': True,
                    'drinks': drinks,
                    }), 200


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def retrieve_drink_detail(payload):
    drink_query = Drink.query.all()
    drinks = []
    drink_query = Drink.query.order_by(Drink.id).all()
    for drink in drink_query:
        drinks.append(drink.long())
    if len(drinks) == 0:
        abort(404)
    return jsonify({'success': True,
                    'drinks': drinks,
                    }), 200

@app.route('/drinks', methods=['POST'])
#@requires_auth('post:drinks')
def create_drink():#(payload):
    body = request.get_json()
    # the required datatype is [{'color': string, 'name':string,
    # 'parts':number}]
    new_title = body.get('title', None)
    new_recipe = body.get('recipe', None)
    # new_recipe = [body.get('recipe', None)] 
    # this was used for postman test 
    try:
        new_drink = Drink(title=new_title, recipe=json.dumps(new_recipe))
        new_drink.insert()
        return jsonify({'success': True,
                        'drinks': [new_drink.long()],
                        }), 200
    except BaseException:
        abort(422)


@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(payload, drink_id):
    drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
    if drink is None:
        abort(404)
    body = request.get_json()
    update_recipe = body.get('recipe', None)
    try:
        drink.recipe = json.dumps(update_recipe)
        drink.update()
        return jsonify({'success': True,
                        'drinks': [drink.long()],
                        }), 200
    except BaseException:
        abort(422)


@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, drink_id):
    drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
    if drink is None:
        abort(404)
    try:
        drink.delete()
        return jsonify({'success': True,
                        'delete': drink_id,
                        }), 200
    except BaseException:
        abort(422)


# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False,
                    "error": 422,
                    "message": "unprocessable"
                    }), 422


@app.errorhandler(404)
def not_found(error):
    return jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404


@app.errorhandler(AuthError)
def auth_error(AuthError):
    return jsonify({
        "success": False,
        "error code": AuthError.status_code,
        "discription": AuthError.error
    }), AuthError.status_code


@app.errorhandler(JWTError)
def jwt_error(e):
    return jsonify({
        "success": False,
        "error code": 401,
        "discription": str(e),
    }), 401
