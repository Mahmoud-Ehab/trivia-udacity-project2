import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.exceptions import HTTPException, NotFound, UnprocessableEntity
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
    @DONE:
    Set up CORS. Allow '*' for origins. Delete the sample route after
    completing the TODOs
    '''
    CORS(app, resources={r'/*': {"origins": '*'}})

    '''
    @DONE: Use the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type, Authorization')

        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET, POST, DELETE')

        return response

    '''
    @DONE:
    Create an endpoint to handle GET requests
    for all available categories.
    '''
    @app.route("/categories", methods=["GET"])
    def get_categories():
        categories = Category.query.all()

        # Create an dict, that maps each category id to its type
        categories_obj = {}
        for category in categories:
            format = category.format()
            categories_obj[format['id']] = format['type']

        response = {
            'categories': categories_obj,
        }

        return jsonify(response)

    '''
    @DONE:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom
     of the screen for three pages.
    Clicking on the page numbers should update the questions.
    '''
    @app.route("/questions", methods=["GET"])
    def get_questions():
        questions_limit = request.args.get('limit', 10, type=int)
        page_num = request.args.get('page', 1, type=int)
        offset = (page_num - 1) * questions_limit

        questions = Question.query.limit(questions_limit).offset(offset).all()
        categories = Category.query.all()

        # Create an dict, that maps each category id to its type
        categories_obj = {}
        for c in categories:
            format = c.format()
            categories_obj[format['id']] = format['type']

        response = {
            'questions': [q.format() for q in questions],
            'total_questions': Question.query.count(),
            'current_category': None,
            'categories': categories_obj
        }

        return jsonify(response)

    '''
    @DONE:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question,
    the question will be removed. This removal will persist
    in the database and when you refresh the page.
    '''
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        try:
            question = Question.query.filter_by(id=question_id).one()
            question.delete()

            return jsonify({
                'success': True,
                'message': f"Question {question_id} has been deleted."
            })

        except:
            abort(404)

    '''
    @DONE:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at
    the end of the last page of the questions list in the "List" tab.
    '''
    @app.route("/questions", methods=["POST"])
    def post_question():
        try:
            body = request.get_json()

            new_question = Question(body['question'],
                                    body['answer'],
                                    int(body['category']),
                                    int(body['difficulty']))

            new_question.insert()

            return jsonify({
                'success': True,
                'message': 'A new question has been added.'
            })

        except:
            abort(422)

    '''
    @DONE:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    '''
    @app.route("/questions/search", methods=["POST"])
    def search_quesion():
        try:
            search_term = request.get_json()['searchTerm']
            questions = Question.query.filter(
                            Question.question.ilike(f"%{search_term}%")
                        ).all()

            response = {
                'questions': [q.format() for q in questions],
                'total_questions': len(questions),
                'current_category': None,
            }

            return jsonify(response)

        except:
            abort(422)

    '''
    @DONE:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    '''
    @app.route("/categories/<int:category_id>/questions", methods=["GET"])
    def get_questions_by_category(category_id):
        try:
            category = Category.query.get(category_id)

            if category is None:
                raise NotFound

            questions = category.questions

            response = {
                'questions': [q.format() for q in questions],
                'total_questions': len(questions),
                'current_category': category.format()
            }

            return jsonify(response)

        except HTTPException as e:
            abort(e.code)

    '''
    @DONE:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    '''
    @app.route("/quizzes", methods=["POST"])
    def play_quiz():
        try:
            prev_questions_ids = request.get_json()['previous_questions']
            category_id = request.get_json()['quiz_category']['id']

            # Initialize the questions list
            category = Category.query.get(category_id)

            if category:
                questions = category.questions
            else:
                questions = Question.query.all()

            # Initialize random question with id None
            rand_q = {'id': None}  # Random question object

            while not rand_q['id'] or rand_q['id'] in prev_questions_ids:
                # If there are no more question.. break the loop
                if len(questions) == 0:
                    rand_q = None
                    break

                # Get random question
                rand_num = random.randint(0, len(questions) - 1)
                rand_q = questions[rand_num].format()

                # Delete the question from the list
                del questions[rand_num]

            # Initialize the response object & return it
            response = {
                'question': rand_q
            }
            return jsonify(response)

        except:
            abort(422)

    '''
    @DONE:
    Create error handlers for all expected errors
    including 404 and 422.
    '''
    @app.errorhandler(HTTPException)
    def general_error_handler(error):
        return jsonify({
            'success': False,
            'error': error.code,
            'message': str(error)
        }), error.code

    return app
