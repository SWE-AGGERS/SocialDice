import unittest
from monolith import app


class SignupTestCase(unittest.TestCase):

    def testSignupPage(self):
        tester = self.getTester()
        response = tester.get('/signup', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def testSuccessfulSignup(self):
        tester = self.getTester()
        user = dict(firstname="Selman",
                    lastname="Alpdündar",
                    email="selman@hotmail.com",
                    dateofbirth=1994,
                    password="123456")
        response = signup(client=tester, data=user)
        assert b'Index Page' in response.data

    def testUnsuccessfulSignup(self):
        tester = self.getTester()
        user = dict(firstname="Selman",
                    lastname="Alpdündar",
                    email="selman@hotmail.com",
                    dateofbirth=1994,
                    password="123456")
        response = signup(client=tester, data=user)
        assert b'The email was used before. Please change the email!' in response.data

    def getTester(self):
        application = app.create_app()
        tester = application.test_client(self)
        return tester


def signup(client, data):
    return client.post('/signup',
                       data=data,
                       follow_redirects=True)
