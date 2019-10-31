import unittest
import json
from flask import request, jsonify
from monolith.app import create_app
from monolith.database import db, User, Story

class TestNewStory(unittest.TestCase):
    def test_create_after_roll(self):
        
        tested_app = create_app()
        with tested_app.test_client() as client:

            # roll the dice
            reply = client.get('/rolldice/5/basic')
            assert b'You\'ve got' in reply.data


if __name__ == '__main__':
    unittest.main()