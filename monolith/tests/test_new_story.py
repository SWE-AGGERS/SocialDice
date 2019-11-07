import unittest
import json
from flask import request, jsonify
from monolith.app import create_app
from monolith.database import db, User, Story
from monolith.tests.restart_db import restart_db_tables
import sys

_app = None

class TestNewStory(unittest.TestCase):
    def test_roll(self):

        global _app
        if _app is None:
            tested_app = create_app(debug=True)
            _app = tested_app
        else:
            tested_app = _app
        restart_db_tables(db, tested_app)

        with tested_app.test_client() as client:


            # login
            reply = login(client, 'example@example.com', 'admin')
            self.assertEqual(reply.status_code, 200)


            # wrong dice number
            reply = client.get('/rolldice/12/basic')
            assert b'Error!' in reply.data

            # non-existing dice set
            reply = client.get('/rolldice/6/pippo')
            self.assertEqual(reply.status_code, 404)

            # correct roll
            reply = client.get('/rolldice/5/basic')

            self.assertEqual(reply.status_code, 200)

            #assert b'Type your story' in reply.data

    def test_valid_post(self):




        global _app
        if _app is None:
            tested_app = create_app(debug=True)
            _app = tested_app
        else:
            tested_app = _app
        restart_db_tables(db, tested_app)

        with tested_app.test_client() as client:





            # login
            reply = login(client, 'example@example.com', 'admin')
            assert b'Hi Admin!' in reply.data
            reply = client.get('/stories')
            assert b'Trial story of example admin user' in reply.data




            # post a new story
            roll = json.dumps(["bird", "whale", "coffee", "bananas", "ladder", "glasses"])



            reply = client.post('/stories', data=dict(text="bird whale coffee bananas ladder glasses", roll=roll), follow_redirects=True)


            self.assertEqual(reply.status_code, 200)

            assert b'bird whale coffee bananas ladder glasses' in reply.data
            # check database entry
            q = db.session.query(Story).order_by(Story.id.desc()).first()
            self.assertEqual(q.text, "bird whale coffee bananas ladder glasses")
            self.assertEqual(q.dicenumber, 6)




    def test_invalid_post(self):




        global _app
        if _app is None:
            tested_app = create_app(debug=True)
            _app = tested_app
        else:
            tested_app = _app
        restart_db_tables(db, tested_app)

        with tested_app.test_client() as client:





            # login
            reply = login(client, 'example@example.com', 'admin')
            assert b'Hi Admin!' in reply.data
            reply = client.get('/stories')
            assert b'Trial story of example admin user' in reply.data




            # post a new story
            roll = json.dumps(["bird", "whale", "coffee", "bananas", "ladder", "glasses"])


            reply = client.post('/stories', data=dict(text="Just a new story for test purposes!", roll=roll), follow_redirects=True)

            self.assertEqual(reply.status_code, 200)

            #print(reply.data)

            assert b'Invalid story. Try again!' in reply.data

            # check database entry
            q = db.session.query(Story).order_by(Story.id.desc()).first()
            self.assertNotEqual(q.text, "Just a new story for test purposes!")








    def test_invalid_post_short_story(self):




        global _app
        if _app is None:
            tested_app = create_app(debug=True)
            _app = tested_app
        else:
            tested_app = _app
        restart_db_tables(db, tested_app)

        with tested_app.test_client() as client:





            # login
            reply = login(client, 'example@example.com', 'admin')
            assert b'Hi Admin!' in reply.data
            reply = client.get('/stories')
            assert b'Trial story of example admin user' in reply.data




            # post a new story
            roll = json.dumps(["bird", "whale", "coffee", "bananas", "ladder", "glasses"])


            reply = client.post('/stories', data=dict(text="short story", roll=roll), follow_redirects=True)

            self.assertEqual(reply.status_code, 200)

            assert b'The number of words of the story must greater or equal of the number of resulted faces.' in reply.data

            # check database entry
            q = db.session.query(Story).order_by(Story.id.desc()).first()
            self.assertNotEqual(q.text, "short story")







    def test_invalid_post_too_long_story(self):




        global _app
        if _app is None:
            tested_app = create_app(debug=True)
            _app = tested_app
        else:
            tested_app = _app
        restart_db_tables(db, tested_app)

        with tested_app.test_client() as client:





            # login
            reply = login(client, 'example@example.com', 'admin')
            assert b'Hi Admin!' in reply.data
            reply = client.get('/stories')
            assert b'Trial story of example admin user' in reply.data




            # post a new story
            roll = json.dumps(["bird", "whale", "coffee", "bananas", "ladder", "glasses"])


            text = ""
            for i in range(0,2000):
                text = text + " a"

            print('ERROR 2', file=sys.stderr)

            reply = client.post('/stories', data=dict(text=text, roll=roll), follow_redirects=True)

            self.assertEqual(reply.status_code, 200)

            assert b'The story is too long' in reply.data

            # check database entry
            q = db.session.query(Story).order_by(Story.id.desc()).first()
            self.assertNotEqual(q.text, text)








def login(client, username, password):
    return client.post('/login', data=dict(
        email=username,
        password=password
    ), follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)

if __name__ == '__main__':
    unittest.main()