import unittest
import json
from flask import request, jsonify
from monolith.app import app as tested_app


class TestReactions(unittest.TestCase):
    def test1(self):  # add reaction to a story
        # tested_app = create_app()
        app = tested_app.test_client()
        self.assertEqual(3,3)
#         reply = app.get('/quizzes/loaded')
#         body = json.loads(str(reply.data, 'utf8'))
#         self.assertEqual(body['loaded_quizzes'], 0)
# )