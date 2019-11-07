import datetime
import unittest

from monolith.app import create_app
from monolith.database import Story, User, db
from monolith.tests.restart_db import restart_db_tables

_app = None

class TestStoryFilter(unittest.TestCase):
    def test1(self):
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

            reply = client.get('/stories/filter')
            self.assertIn(b'Filter Stories', reply.data)

            # Filter correctly a time interval
            reply = client.post('/stories/filter', data=dict(
                init_date='2019-01-01',
                end_date='2019-12-01'
            ), follow_redirects=True)
            self.assertIn(b'Trial story of example', reply.data)

            # Filter wrongly a time interval (init_date > end_date)
            reply = client.post('/stories/filter', data=dict(
                init_date='2019-12-01',
                end_date='2019-01-01'
            ), follow_redirects=True)
            self.assertIn(b'Cant travel back in time', reply.data)

    def test2(self):
        global _app
        if _app is None:
            tested_app = create_app(debug=True)
            _app = tested_app
        else:
            tested_app = _app
        # create 100 Stories
        restart_db_tables(db, tested_app)
        with tested_app.test_client() as client:
            # login
            reply = login(client, 'example@example.com', 'admin')
            assert b'Hi Admin!' in reply.data


def login(client, username, password):
    return client.post('/login', data=dict(
        email=username,
        password=password
    ), follow_redirects=True)
