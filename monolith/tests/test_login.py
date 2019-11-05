import unittest
from monolith import app


class LoginTestCase(unittest.TestCase):

    def testLoginPage(self):
        response = self.getTester.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def testUnsuccessfulLogin(self):
        tester = self.getTester
        reply = login(tester, "selman@hotmail", "12345")
        assert b'User not found' in reply.data

    def testSuccessfulLogin(self):
        tester = self.getTester
        reply = login(tester, "example@example.com", "admin")
        assert b'Index Page' in reply.data

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

