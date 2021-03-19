import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app, QUESTIONS_PER_PAGE
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        # Initialize database_path
        self.DB_USER = os.getenv("DB_USER", "postgres")
        self.DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
        self.DB_HOST = os.getenv("DB_HOST", "localhost:5432")
        self.DB_NAME = os.getenv("DB_NAME", "trivia_test")

        self.database_path = "postgresql://{}:{}@{}/{}".format(
            self.DB_USER, self.DB_PASSWORD,
            self.DB_HOST, self.DB_NAME
            )

        # Make db connection
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    DONE:
    Write at least one test for each test for successful
    operation and for expected errors.
    """
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data['questions']), QUESTIONS_PER_PAGE)
        self.assertEqual(data['total_questions'], Question.query.count())
        self.assertTrue(data['categories'])

    def test_post_question(self):
        new_question = {
            'question': 'test',
            'answer': 'test',
            'category': 1,
            'difficulty': 1
        }
        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

        last_question = Question.query.order_by(Question.id.desc()).first()
        self.assertSequenceEqual(
            last_question.question,
            new_question['question'])

    def test_delete_question(self):
        last_question_id = Question.query.order_by(
                Question.id.desc()
            ).first().id

        res = self.client().delete('/questions/' + str(last_question_id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(Question.query.get(last_question_id), None)

    def test_search(self):
        res = self.client().post(
            '/questions/search',
            json={'searchTerm': 'what'})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])

    def test_category_questions(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

    def test_quizzes(self):
        req_body = {
            'quiz_category': {'id': 1},
            'previous_questions': []
        }
        res = self.client().post('/quizzes', json=req_body)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['question'])

    # -------------------------------------
    # Test Errors handlers
    # -------------------------------------
    def test_notfound(self):
        res = self.client().get('/SomeTestEndpoint')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertTrue(not data['success'])
        self.assertTrue(data['error'])
        self.assertTrue(data['message'])

    def test_unprocessable(self):
        res = self.client().post('/quizzes')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertTrue(not data['success'])
        self.assertTrue(data['error'])
        self.assertTrue(data['message'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
