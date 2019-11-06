import unittest
from monolith import app
from monolith.auth import load_user, admin_required
from monolith.database import User
from flask_login import  current_user
class AuthTestCase(unittest.TestCase):

    def testLoadUser(self):
        load_user(user_id=current_user)

    @property
    def getTester(self):
        application = app.create_app()
        tester = application.test_client(self)
        return tester

def login(client, username, password):
    return client.post('/login', data=dict(
        email=username,
        password=password
    ), follow_redirects=True)

