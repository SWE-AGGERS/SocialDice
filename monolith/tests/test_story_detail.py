import unittest

from monolith.app import create_app


class TestApp(unittest.TestCase):
    def test1(self):
        app = create_app().test_client()
        reply = app.get('/stories/1')
        self.assertEqual(reply.status_code, 200)

    def test2(self):
        app = create_app().test_client()
        reply = app.get('/stories/nonExistingID')
        self.assertEqual(reply.status_code, 404)
