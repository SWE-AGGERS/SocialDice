import unittest
import json
from flask import request, jsonify
from monolith.app import create_app


class TestApp(unittest.TestCase):
    def test1(self):
        app = create_app().test_client()
        reply = app.get('/stories/1')
        self.assertIn('author: Admin', str(reply.data))
        self.assertIn('likes: 42', str(reply.data))

    def test2(self):
        app = create_app().test_client()
        reply = app.get('/stories/1')
        self.assertEqual(reply.status_code, 200)

    def test3(self):
        app = create_app().test_client()
        reply = app.get('/stories/12')
        self.assertEqual(reply.status_code, 404)
