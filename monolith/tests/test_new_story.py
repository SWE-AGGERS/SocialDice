import unittest
import json
from flask import request, jsonify
from monolith.app import create_app
from monolith.database import db, User, Story

class TestNewStory(unittest.TestCase):
    def test_roll(self):
        
        tested_app = create_app()
        with tested_app.test_client() as client:

            # roll the dice
            reply = client.get('/rolldice/5/basic')
            #print(reply.data)
            assert b'You\'ve got' in reply.data

    def test_post(self):
        tested_app = create_app(debug=True)
        with tested_app.test_client() as client:
            # login
            reply = login(client, 'example@example.com', 'admin')
            assert b'Hi Admin!' in reply.data
            reply = client.get('/stories')
            assert b'Trial story of example admin user' in reply.data

            # post a new story 
            roll = json.dumps(["bike", "tulip", "happy", "cat", "ladder", "rain"])
            reply = client.post('/stories', data=dict(text="Just a new story for test purposes!", roll=roll), follow_redirects=True)
            assert b'Just a new story for test purposes!' in reply.data
            # check database entry
            q = db.session.query(Story).order_by(Story.id.desc()).first()
            self.assertEqual(q.text, "Just a new story for test purposes!")
            self.assertEqual(q.dicenumber, 6)



def login(client, username, password):
    return client.post('/login', data=dict(
        email=username,
        password=password
    ), follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)

if __name__ == '__main__':
    unittest.main()