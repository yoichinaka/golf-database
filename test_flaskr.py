import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Player, Course, Score
#from test_token import course_manager_token, player1_token, player2_token

course_manager_token=os.environ['course_manager_token']
player1_token=os.environ['player1_token']
player2_token=os.environ['player2_token']

class GolfTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app)

        # # binds the app to the current context
        # with self.app.app_context():
        #     self.db = SQLAlchemy()
        #     self.db.init_app(self.app)
        #     # create all tables
        #     self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    Write at least one test for each test for successful operation and for expected errors.
    GET '/players'
    POST '/players' need permissions
    GET '/courses'
    POST '/courses' need permissions
    GET '/scores'
    GET '/players/<int:player_id>/scores'
    POST '/players/<int:player_id>/scores' need permissions
    PATCH '/players/<int:player_id>/scores/<int:score_id>' need permissions
    DELETE '/players/<int:player_id>/scores/<int:score_id>' need permissions
    """

    def test_delete_player_score(self):
        # Delete score_id=7 from player_id=1,
        # by inputing palyer_id=1's JWT token.
        res = self.client().delete(
            '/players/1/scores/7',
            headers={
                'Authorization': 'bearer ' + player1_token},
        )
        self.assertEqual(res.status_code, 200)

    def test_fail_delete_player_score(self):
        # Using fake JWT, it should be error.
        res = self.client().delete('/players/1/scores/7',
                                   headers={'Authorization': 'bearer ' + 'dummy_token'})
        self.assertEqual(
            json.loads(
                res.data).get('discription'),
            'Error decoding token headers.')
        self.assertEqual(res.status_code, 401)

    def test_patch_player_score(self):
        new_score = {
            'score': '90',
            'course_id': '1'
        }
        res = self.client().patch(
            '/players/1/scores/3',
            headers={
                'Authorization': 'bearer ' + player1_token},
            json=new_score)
        self.assertEqual(res.status_code, 200)

    def test_fail_patch_player_score(self):
        # Using fake JWT, it should be error.
        new_score = {
            'score': '90',
            'course_id': '1'
        }
        res = self.client().patch(
            '/players/1/scores/3',
            headers={
                'Authorization': 'bearer ' + 'dummy_token'},
            json=new_score)
        self.assertEqual(
            json.loads(
                res.data).get('discription'),
            'Error decoding token headers.')
        self.assertEqual(res.status_code, 401)

    def test_post_player_score(self):
        # This test is checking Auth process with player1 JWT token.
        new_score = {
            'player_id': '1',
            'course_id': '2',
            'score': '90',
            'date': '20210331'
        }
        res = self.client().post(
            '/players/1/scores',
            headers={
                'Authorization': 'bearer ' + player1_token},
            json=new_score)

        self.assertEqual(res.status_code, 200)

    def test_fail_post_player_score(self):
        # Using fake JWT, it should be error.
        new_score = {
            'player_id': '1',
            'course_id': '2',
            'score': '90',
        }
        res = self.client().post(
            '/players/1/scores',
            headers={
                'Authorization': 'bearer ' + 'dummy_token'},
            json=new_score)
        self.assertEqual(
            json.loads(
                res.data).get('discription'),
            'Error decoding token headers.')
        self.assertEqual(res.status_code, 401)

    def test_post_courses(self):
        # This test is checking Auth process with course manager's JWT token.
        new_course = {
            'name': 'test_course',
                    'state': 'Tokyo',
                    'image_link': 'www1',
        }
        res = self.client().post(
            '/courses',
            headers={
                'Authorization': 'bearer ' + course_manager_token},
            json=new_course)

        self.assertEqual(res.status_code, 200)

    def test_fail_post_courses(self):
        # Using fake JWT, it should be error.
        new_course = {
            'name': 'test_course',
                    'state': 'Tokyo',
                    'image_link': 'www1',
        }
        res = self.client().post(
            '/courses',
            headers={
                'Authorization': 'bearer ' + 'dummy_token'},
            json=new_course)
        self.assertEqual(
            json.loads(
                res.data).get('discription'),
            'Error decoding token headers.')
        self.assertEqual(res.status_code, 401)

    def test_post_players(self):
        # This test is checking Auth process with player2's JWT token.
        new_player = {
            'name': 'player2',
                    'image_link': 'www2',
        }
        res = self.client().post(
            '/players',
            headers={
                'Authorization': 'bearer ' + player2_token},
            json=new_player)
        self.assertEqual(res.status_code, 200)

    def test_fail_post_players(self):
        # Using fake JWT, it should be error.
        new_player = {
            'name': 'test_player2',
                    'image_link': 'www1',
        }
        res = self.client().post(
            '/players',
            headers={
                'Authorization': 'bearer ' + 'dummytoken'},
            json=new_player)
        self.assertEqual(
            json.loads(
                res.data).get('discription'),
            'Error decoding token headers.')
        self.assertEqual(res.status_code, 401)

    def test_get_players(self):
        # Get all players data, status should be 200.
        res = self.client().get('/players')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['players'])

    def test_fail_get_players(self):
        # Test will be fail because of the wrong URL.
        res = self.client().get('/player')
        self.assertEqual(res.status_code, 404)

    def test_get_courses(self):
        # Get all course data, status should be 200.
        res = self.client().get('/courses')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['courses'])

    def test_fail_get_courses(self):
        # Test will be fail because of the wrong URL.
        res = self.client().get('/course')
        self.assertEqual(res.status_code, 404)

    def test_get_scores(self):
        # Get all score from all players, status should be 200.
        res = self.client().get('/scores')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['scores'])

    def test_fail_get_scores(self):
        # Test will be fail because of the wrong URL.
        res = self.client().get('/score')
        self.assertEqual(res.status_code, 404)

    def test_get_players_scores(self):
        # Get the all scores from players_id=6. status should be 200.
        # the number of score should be 2.
        res = self.client().get('/players/6/scores')
        data = json.loads(res.data)
        self.assertEqual(len(data.get('scores')), 2)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['scores'])

    def test_fail_get_players_scores(self):
        # Test will be fail because there is not player_id = 100.
        res = self.client().get('/players/100/scores')
        self.assertEqual(res.status_code, 404)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
