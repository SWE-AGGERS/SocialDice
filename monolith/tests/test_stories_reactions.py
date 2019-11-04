import unittest

from monolith.app import create_app


class TestReactions(unittest.TestCase):
    def test1(self):
        tested_app = create_app(debug=True)
        with tested_app.test_client() as client:
            # with client.session_transaction() as sess:

            # login
            reply = login(client, 'example@example.com', 'admin')
            assert b'Hi Admin!' in reply.data
            reply = client.get('/stories')
            assert b'Trial story of example admin user' in reply.data

            # add reaction to a story
            reply = client.get('/story/1/reaction/1')
            assert b'Reaction to story created' in reply.data

            # add same reaction to a story - delete that reaction
            reply = client.get('/story/1/reaction/1')
            assert b'You already react in this way' in reply.data

            # add different reaction to a story
            reply = client.get('/story/1/reaction/2')
            assert b'Reaction to story created' in reply.data

            # change the reaction to a story
            reply = client.get('/story/1/reaction/1')
            assert b'You change your reaction' in reply.data

            # add reaction to non-existing story
            reply = client.get('/story/3/reaction/1')
            assert b'Story doent exist' in reply.data


def login(client, username, password):
    return client.post('/login', data=dict(
        email=username,
        password=password
    ), follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)
