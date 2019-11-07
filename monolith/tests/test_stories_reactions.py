import unittest
import json

from monolith.app import create_app
from monolith.database import db

_app = None


class TestReactions(unittest.TestCase):

    def test1(self):
        global _app
        tested_app = create_app(debug=True)
        _app = tested_app
        with tested_app.test_client() as client:
            with client.session_transaction() as sess:
                db.drop_all()
                db.create_all()

        with tested_app.test_client() as client:
            # Create user
            resp = client.post('/signup',
                       data=dict(firstname="admin_firstname",
                        lastname="admin_lastname",
                        email="admin@example.com",
                        dateofbirth=1994,
                        password="admin"),
                       follow_redirects=True)
            assert b'Index Page' in resp.data

            # login
            reply = login(client, 'admin@example.com', 'admin')
            assert b'Hi admin_firstname!' in reply.data

            # post a new story
            roll = json.dumps(["bike", "tulip", "happy", "cat", "ladder", "rain"])
            reply = client.post('/stories', data=dict(text="bike tulip happy cat ladder rain", roll=roll), follow_redirects=True)
            assert b'bike tulip happy cat ladder rain' in reply.data

            reply = client.get('/stories')
            assert b'bike tulip happy cat ladder rain' in reply.data

            # add reaction to a story
            reply = client.get('/stories/reaction/1/1')
            print(reply.data)
            assert b'Reaction created' in reply.data

            # add same reaction to a story - delete that reaction
            reply = client.get('/stories/reaction/1/1')
            assert b'Reaction removed!' in reply.data

            # add different reaction to a story
            reply = client.get('/stories/reaction/1/2')
            assert b'Reaction created' in reply.data

            # change the reaction to a story
            reply = client.get('/stories/reaction/1/1')
            assert b'Reaction changed!' in reply.data

            # add reaction to non-existing story
            reply = client.get('/stories/reaction/3/1')
            assert b'Story not exists!' in reply.data


def login(client, username, password):
    return client.post('/login', data=dict(
        email=username,
        password=password
    ), follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)
