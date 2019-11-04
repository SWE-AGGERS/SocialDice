import unittest
from monolith import app


class LogoutTestCase(unittest.TestCase):

    def testlogout(self):
        client = self.getTester
        response = logout(client=client)
        print(response.data)
        assert b'Hi Anonymous' in response.data

    @property
    def getTester(self):
        application = app.create_app()
        tester = application.test_client(self)
        return tester


def logout(client):
    return client.get('/logout',
                      follow_redirects=True)
