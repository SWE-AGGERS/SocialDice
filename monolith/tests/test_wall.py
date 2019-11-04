import datetime
import unittest
import json
from flask import request, jsonify
from monolith.app import create_app
from monolith.classes.Wall import Wall
from monolith.database import db, User, Story, Reaction


test_app = create_app()
test_app.app_context().push()


class MyTestCase(unittest.TestCase):
    def test_something(self):
        app = test_app.test_client()
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
            example.dislikes = 0
            example.author_id = user.id
            print(example)
            db.session.add(example)

            example = Story()
            example.text = 'Leaving just a memory...Snapshot in the family album...Daddy what else did you leave for me?'
            example.likes = 42
            example.dislikes = 0
            example.author_id = user.id
            print(example)
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

        reply = app.get('/wall/' + str(user.id))
        body = json.loads(str(reply.data, 'utf8'))

        self.assertEqual(body, {
            "firstname" : user.firstname,
            "lastname": user.lastname,
            "email": user.email,
            "stories": stories #thewalltest.stories
        })




if __name__ == '__main__':
    unittest.main()
