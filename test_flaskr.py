import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format(
            'localhost:5432', self.database_name)
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
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    GET '/categories'
    GET '/questions'
    GET '/categories/<int:category_id>/questions'
    DELETE '/questions/<int:question_id>'
    POST '/questions'
    POST 'questions/seach'
    POST 'quizzes'
    """

    def test_get_categries(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])

    def test_fail_get_categries(self):
        # input wrong URL
        res = self.client().get('/category')

        self.assertEqual(res.status_code, 404)

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])

    def test_fail_get_questions(self):
        # There is not page 100, it should return '404'.
        res = self.client().get('/questions?page=100')

        self.assertEqual(res.status_code, 404)

    def test_get_category_id_questions(self):
        res = self.client().get('categories/1/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['current_category'], 1)
        self.assertEqual(data['total_questions'], 3)
        self.assertTrue(data['questions'])

    def test_fail_get_category_id_questions(self):
        # There is not category 10, it should return '404'.
        res = self.client().get('categories/10/questions')

        self.assertEqual(res.status_code, 404)

    def test_delete_questions(self):
        res = self.client().delete('/questions/11')
        question = Question.query.filter(Question.id == 11).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(question, None)

    def test_fail_delete_questions(self):
        # there is not question number 100,
        res = self.client().delete('/questions/100')

        self.assertEqual(res.status_code, 404)

    def test_post_questions_post(self):
        # After post a new quesition, this test gets the new question from database
        # and check if the returned value is same as the post value.
        # The new question id should be no.24 in this case.
        new_question = {
            'question': 'new qeustion',
                        'answer': 'new answer',
                        'category': '1',
                        'difficulty': '3'
        }
        res = self.client().post('/questions',
                                 json=new_question)
        question = Question.query.filter(Question.id == 24).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(question.format()['question'], 'new qeustion')
        self.assertEqual(question.format()['answer'], 'new answer')
        self.assertEqual(question.format()['difficulty'], 3)
        self.assertEqual(question.format()['category'], 1)

    def test_fail_post_questions_post(self):
        # The difficulty must be integer.
        # In this test,'difficulty is 'a' mistakenly,
        # so,it should return 422 error code.
        new_question = {
            'question': 'new qeustion',
                        'answer': 'new answer',
                        'category': '1',
                        'difficulty': 'a'
        }
        res = self.client().post('/questions',
                                 json=new_question)

        self.assertEqual(res.status_code, 422)

    def test_search_questions(self):
        res = self.client().post('/questions/search',
                                 json={'searchTerm': 'title'})
        data = json.loads(res.data)
        # The number of questions which include 'title' must be 2.
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['total_questions'], 2)

    def test_fail_search_questions(self):
        # When POST json body is empty, it should return '400'
        res = self.client().post('/questions/search',
                                 )
        self.assertEqual(res.status_code, 400)

    def test_quizzes(self):
        # When client POST quizzes request, it return a question object
        # randomly from a given category.

        res = self.client().post(
            '/quizzes',
            json={
                "previous_questions": [20],
                "quiz_category": {
                    "type": "Science",
                    "id": "1"}})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('question').get('category'), 1)

    def test_fail_quizzes(self):
        # When id number is not valid, it rutruns 422 error.
        res = self.client().post(
            '/quizzes',
            json={
                "previous_questions": [20],
                "quiz_category": {
                    "type": "Science",
                    "id": "10"}})
        self.assertEqual(res.status_code, 422)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
