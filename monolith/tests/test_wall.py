import datetime
import random
import unittest
import json
from flask import request, jsonify
from monolith.app import create_app
from monolith.classes.Wall import Wall
from monolith.database import db, User, Story
from monolith.tests.test_stories_reactions import login

test_app = create_app(debug=True)
test_app.app_context().push()


class WallTestCase(unittest.TestCase):
    def test_json_wall(self):
        app = test_app.test_client()

        with app.session_transaction() as sess:
            db.drop_all()
            db.create_all()

        q = db.session.query(User).filter(User.email == 'user@waltest.com')
        user = q.first()
        if user is None:
            example = User()
            example.firstname = 'userwall'
            example.lastname = 'theWall'
            example.email = 'user@waltest.com'
            example.dateofbirth = datetime.datetime(2020, 10, 5)
            example.is_admin = True
            example.set_password('daddysflownacrosstheocean')
            db.session.add(example)
            db.session.commit()
            q = db.session.query(User).filter(User.email == 'user@waltest.com')
            user = q.first()

        q = db.session.query(Story).filter(Story.author_id == user.id)
        story = q.first()
        if story is None:

            example = Story()
            example.text = 'We dont need no education We dont need no...All in all you re just another brick in the wall'
            example.likes = 42
            example.dislikes = 1
            example.dicenumber = 6
            example.author_id = user.id
            db.session.add(example)

            example = Story()
            example.text = 'Leaving just a memory...Snapshot in the family album...Daddy what else did you leave for me?'
            example.likes = 42
            example.dislikes = 0
            example.dicenumber = 4
            example.author_id = user.id
            db.session.add(example)

            db.session.commit()
            q = db.session.query(Story).filter(Story.author_id == user.id)

        stories = []
        thewalltest = Wall(user)
        for s in q:
            s: Story
            thewalltest.add_story(s)
            stories.append(
                {'story_id': s.id,
                 'text': s.text,
                 'likes': s.likes,
                 'dislikes': s.dislikes})

        reply = app.get('/thewall/' + str(user.id))
        body = json.loads(str(reply.data, 'utf8'))

        self.assertEqual(body, {
            "id": user.id,
            "firstname" : user.firstname,
            "lastname": user.lastname,
            "email": user.email,
            "stories": stories  # thewalltest.stories
        })

        wall_repl = Wall()
        wall_repl.acquire_from_json(reply)
        self.assertEqual(thewalltest.id, wall_repl.id, "Json acquire fail")

    def test_json_wall_fail(self):
        app = test_app.test_client()
        reply = login(app, 'user@waltest.com', 'daddysflownacrosstheocean')

        reply = app.get('/thewall/' + '-1')

        self.assertIn('User NOT Found', str(reply.data))

    def test_mywall(self):

        app = test_app.test_client()

        reply = login(app, 'user@waltest.com', 'daddysflownacrosstheocean')

        reply = app.get('/wall')

        self.assertIn('user@waltest.com', str(reply.data))

    def test_wall(self):
        app = test_app.test_client()

        reply = login(app, 'user@waltest.com', 'daddysflownacrosstheocean')

        q = db.session.query(User).filter(User.email == 'user@waltest.com')
        user: User = q.first()

        reply = app.get('/wall/' + str(user.id))

        self.assertIn(user.email, str(reply.data))

        q = db.session.query(Story).filter(Story.author_id == user.id)

        for s in q:
            s: Story
            self.assertIn(s.text, str(reply.data))



    def test_wall_fail(self):
        app = test_app.test_client()

        reply = login(app, 'user@waltest.com', 'daddysflownacrosstheocean')

        reply = app.get('/wall/' + '-1')

        self.assertIn('User NOT Found', str(reply.data))


class TestWallClass(unittest.TestCase):

    def test_die_init(self):
        example = User()
        example.id = random.randint(0, 2048)
        example.firstname = 'userwall'
        example.lastname = 'theWall'
        example.email = 'user@waltest.com'
        example.dateofbirth = datetime.datetime(2020, 10, 5)
        example.is_admin = True
        example.set_password('daddysflownacrosstheocean')

        some_stories = ['story1', 'story2', 'story3', 'story4', 'story5', 'story6']

        wall = Wall(example)

        for s in some_stories:
            story = Story()
            story.id = random.randint(0, 2048)
            story.text = s
            story.likes = 0
            story.dislikes = 0
            wall.add_story(story)

        wall.storyLimit = len(wall.stories)

        story = Story()
        story.id = random.randint(0, 2048)
        story.text = 'an extra story'
        story.likes = 0
        story.dislikes = 0
        wall.add_story(story)

        wall.add_story(story)

        self.assertEqual(len(wall.stories), wall.storyLimit)

if __name__ == '__main__':
    unittest.main()
