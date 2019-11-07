import unittest

from monolith.app import create_app


class TestRandomStory(unittest.TestCase):
    def test_story_retrieval(self):
        tested_app = create_app(debug=True)
        with tested_app.test_client() as client:
            reply = client.get('/stories/random', content_type='html/text',follow_redirects=True)
            self.assertIn('<div class="card text-center">', str(reply.data))


if __name__ == '__main__':
    unittest.main()
