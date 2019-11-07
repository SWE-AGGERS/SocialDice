import unittest
from monolith import app


class SearchTestCase(unittest.TestCase):

    def testUserSearch(self):
        client = self.getTester
        login(client, "example@example.com", "admin")
        response = search(client, "Admin")
        assert b'Admin' in response.data

    def test_story_and_user_search(self):
        client = self.getTester
        login(client, "example@example.com", "admin")
        response = search(client, "admin")
        assert b'Admin' in response.data

    def testNotFound(self):
        client = self.getTester
        login(client, "example@example.com", "admin")
        response = search(client, "ssssss")
        assert b'Search Results' in response.data

    def testNullParameter(self):
        client = self.getTester
        login(client, "example@example.com", "admin")
        response = search_without_text(client)
        assert b'Search Results' in response.data

    def test_search_with_list(self):
        client = self.getTester
        login(client, "example@example.com", "admin")
        response = search(client, "Admin Admin")
        assert b'Admin' in response.data

    @property
    def getTester(self):
        application = app.create_app()
        tester = application.test_client(self)
        return tester


def search(client, text):
    return client.get('/search', query_string={'search_text': text}, follow_redirects=True)


def search_without_text(client):
    return client.get('/search', follow_redirects=True)


def login(client, username, password):
    return client.post('/login', data=dict(
        email=username,
        password=password
    ), follow_redirects=False)
