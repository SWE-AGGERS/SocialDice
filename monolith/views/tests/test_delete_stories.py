import unittest
from monolith.app import create_app
from monolith.tests.test_stories_reactions import login, logout
from monolith.database import db, Story, Reaction, User
from monolith.database import User
from flask_login import current_user
from monolith.tests.restart_db import restart_db_tables

_app = None


class TestDeleteStory(unittest.TestCase):

    def test_delete_story_positive(self):

        global _app
        if _app is None:
            tested_app = create_app(debug=True)
            _app = tested_app
        else:
            tested_app = _app
        restart_db_tables(db, tested_app)

        with tested_app.test_client() as client:

            # login
            reply = login(client, 'example@example.com', 'admin')
            self.assertEqual(reply.status_code, 200)

            users = User.query.all()
            self.assertEqual(len(users), 1)

            # add reaction to a story
            reply = client.get('/stories/reaction/1/1')
            self.assertEqual(reply.status_code, 200)

            story = db.session.query(Story).filter_by(id=1).first()
            self.assertNotEqual(story, None)

            stories = Story.query.filter_by(id=1).all()
            self.assertEqual(len(stories), 1)

            reactions = Reaction.query.filter_by(story_id=1).all()
            self.assertEqual(len(reactions), 1)

            users = User.query.all()
            self.assertEqual(len(users), 1)

            reply = client.post('stories/1/remove/stories', follow_redirects=True)

            self.assertEqual(reply.status_code, 200)

            assert b'The story has been canceled.' in reply.data

            reactions = Reaction.query.filter_by(story_id=1).all()
            self.assertEqual(len(reactions), 0)

            # logout
            reply = logout(client)
            self.assertEqual(reply.status_code, 200)

    def test_delete_story_negative(self):

        global _app
        if _app is None:
            tested_app = create_app(debug=True)
            _app = tested_app
        else:
            tested_app = _app
        restart_db_tables(db, tested_app)

        with tested_app.test_client() as client:

            # login
            reply = login(client, 'example@example.com', 'admin')
            self.assertEqual(reply.status_code, 200)

            users = User.query.all()
            self.assertEqual(len(users), 1)

            # add reaction to a story
            reply = client.get('/stories/reaction/1/1')
            self.assertEqual(reply.status_code, 200)

            reply = client.post('stories/2/remove/stories', follow_redirects=True)
            self.assertEqual(reply.status_code, 404)

            story = db.session.query(Story).filter_by(id=1).first()
            self.assertNotEqual(story, None)

            reactions = Reaction.query.filter_by(story_id=1).all()
            self.assertEqual(len(reactions), 1)

            stories = Story.query.filter_by(id=1).all()
            self.assertEqual(len(stories), 1)

            users = User.query.all()
            self.assertEqual(len(users), 1)

            reply = client.post('stories/1/remove/stories', follow_redirects=True)
            self.assertEqual(reply.status_code, 200)

            assert b'The story has been canceled.' in reply.data

            reactions = Reaction.query.filter_by(story_id=1).all()
            self.assertEqual(len(reactions), 0)

            # logout
            reply = logout(client)
            self.assertEqual(reply.status_code, 200)

    def test_delete_story_multiple_users_reactions(self):

        global _app
        if _app is None:
            tested_app = create_app(debug=True)
            _app = tested_app
        else:
            tested_app = _app
        restart_db_tables(db, tested_app)

        with tested_app.test_client() as client:

            # login
            reply = login(client, 'example@example.com', 'admin')
            self.assertEqual(reply.status_code, 200)

            # add reaction to a story
            reply = client.get('/stories/reaction/1/1')
            self.assertEqual(reply.status_code, 200)

            users = User.query.all()
            self.assertEqual(len(users), 1)

            story = db.session.query(Story).filter_by(id=1).first()
            self.assertNotEqual(story, None)

            # logout
            reply = logout(client)
            self.assertEqual(reply.status_code, 200)

            # signup
            user1 = User()
            user1.firstname = "Mario"
            user1.lastname = "Rossi"
            user1.email = "mario.rossi@gmail.com"
            user1.dateofbirth = "1994"
            user1.password = user1.set_password("12345")
            reply = signup(client, user1)
            self.assertEqual(reply.status_code, 200)

            users = User.query.all()
            self.assertEqual(len(users), 2)

            stories = Story.query.filter_by(id=1).all()
            self.assertEqual(len(stories), 1)

            reactions = Reaction.query.filter_by(story_id=1).all()
            self.assertEqual(len(reactions), 1)

            story = db.session.query(Story).filter_by(id=1).first()
            self.assertNotEqual(story, None)

            reactions = Reaction.query.filter_by(story_id=1).all()
            self.assertEqual(len(reactions), 1)

            # add reaction to a story
            reply = client.get('/stories/reaction/1/1')
            self.assertEqual(reply.status_code, 200)

            # logout
            reply = logout(client)
            self.assertEqual(reply.status_code, 200)

            # login
            reply = login(client, 'example@example.com', 'admin')
            self.assertEqual(reply.status_code, 200)

            story = db.session.query(Story).filter_by(id=1).first()
            self.assertNotEqual(story, None)

            reactions = Reaction.query.filter_by(story_id=1).all()
            self.assertEqual(len(reactions), 2)

            reply = client.post('stories/1/remove/stories', follow_redirects=True)
            self.assertEqual(reply.status_code, 200)

            assert b'The story has been canceled.' in reply.data

            story = db.session.query(Story).filter_by(id=1).first()
            self.assertEqual(story, None)

            # logout
            reply = logout(client)
            self.assertEqual(reply.status_code, 200)

    def test_delete_wrong_author_story(self):

        global _app
        if _app is None:
            tested_app = create_app(debug=True)
            _app = tested_app
        else:
            tested_app = _app
        restart_db_tables(db, tested_app)

        with tested_app.test_client() as client:

            # login
            reply = login(client, 'example@example.com', 'admin')
            self.assertEqual(reply.status_code, 200)

            # add reaction to a story
            reply = client.get('/stories/reaction/1/1')
            self.assertEqual(reply.status_code, 200)

            users = User.query.all()
            self.assertEqual(len(users), 1)

            story = db.session.query(Story).filter_by(id=1).first()
            self.assertNotEqual(story, None)

            # logout
            reply = logout(client)
            self.assertEqual(reply.status_code, 200)

            # signup
            user1 = User()
            user1.firstname = "Mario"
            user1.lastname = "Rossi"
            user1.email = "mario.rossi@gmail.com"
            user1.dateofbirth = "1994"
            user1.password = user1.set_password("12345")
            reply = signup(client, user1)
            self.assertEqual(reply.status_code, 200)

            users = User.query.all()
            self.assertEqual(len(users), 2)

            story = db.session.query(Story).filter_by(id=1).first()
            self.assertNotEqual(story, None)

            stories = Story.query.filter_by(id=1).all()
            self.assertEqual(len(stories), 1)

            reactions = Reaction.query.filter_by(story_id=1).all()
            self.assertEqual(len(reactions), 1)

            story = db.session.query(Story).filter_by(id=1).first()
            self.assertNotEqual(story, None)

            reactions = Reaction.query.filter_by(story_id=1).all()
            self.assertEqual(len(reactions), 1)

            # add reaction to a story
            reply = client.get('/stories/reaction/1/1')
            self.assertEqual(reply.status_code, 200)

            reply = client.post('stories/1/remove/stories', follow_redirects=True)
            self.assertEqual(reply.status_code, 200)

            assert b'The story was written by another user and cannot be deleted.' in reply.data

            story = db.session.query(Story).filter_by(id=1).first()
            self.assertNotEqual(story, None)

            # logout
            reply = logout(client)
            self.assertEqual(reply.status_code, 200)

    def test_delete_story_positive_index(self):

        global _app
        if _app is None:
            tested_app = create_app(debug=True)
            _app = tested_app
        else:
            tested_app = _app
        restart_db_tables(db, tested_app)

        with tested_app.test_client() as client:

            # login
            reply = login(client, 'example@example.com', 'admin')
            self.assertEqual(reply.status_code, 200)

            users = User.query.all()
            self.assertEqual(len(users), 1)

            # add reaction to a story
            reply = client.get('/stories/reaction/1/1')
            self.assertEqual(reply.status_code, 200)

            story = db.session.query(Story).filter_by(id=1).first()
            self.assertNotEqual(story, None)

            stories = Story.query.filter_by(id=1).all()
            self.assertEqual(len(stories), 1)

            reactions = Reaction.query.filter_by(story_id=1).all()
            self.assertEqual(len(reactions), 1)

            users = User.query.all()
            self.assertEqual(len(users), 1)

            reply = client.post('stories/1/remove/index', follow_redirects=True)
            self.assertEqual(reply.status_code, 200)

            reactions = Reaction.query.filter_by(story_id=1).all()
            self.assertEqual(len(reactions), 0)

            # logout
            reply = logout(client)
            self.assertEqual(reply.status_code, 200)

    def test_delete_story_negative_index(self):

        global _app
        if _app is None:
            tested_app = create_app(debug=True)
            _app = tested_app
        else:
            tested_app = _app
        restart_db_tables(db, tested_app)

        with tested_app.test_client() as client:

            # login
            reply = login(client, 'example@example.com', 'admin')
            self.assertEqual(reply.status_code, 200)

            users = User.query.all()
            self.assertEqual(len(users), 1)

            # add reaction to a story
            reply = client.get('/stories/reaction/1/1')
            self.assertEqual(reply.status_code, 200)

            reply = client.post('stories/2/remove/index', follow_redirects=True)
            self.assertEqual(reply.status_code, 404)

            story = db.session.query(Story).filter_by(id=1).first()
            self.assertNotEqual(story, None)

            reactions = Reaction.query.filter_by(story_id=1).all()
            self.assertEqual(len(reactions), 1)

            stories = Story.query.filter_by(id=1).all()
            self.assertEqual(len(stories), 1)

            users = User.query.all()
            self.assertEqual(len(users), 1)

            reply = client.post('stories/1/remove/index', follow_redirects=True)
            self.assertEqual(reply.status_code, 200)

            reactions = Reaction.query.filter_by(story_id=1).all()
            self.assertEqual(len(reactions), 0)

            # logout
            reply = logout(client)
            self.assertEqual(reply.status_code, 200)

    def test_delete_story_multiple_users_reactions_index(self):

        global _app
        if _app is None:
            tested_app = create_app(debug=True)
            _app = tested_app
        else:
            tested_app = _app
        restart_db_tables(db, tested_app)

        with tested_app.test_client() as client:

            # login
            reply = login(client, 'example@example.com', 'admin')
            self.assertEqual(reply.status_code, 200)

            # add reaction to a story
            reply = client.get('/stories/reaction/1/1')
            self.assertEqual(reply.status_code, 200)

            users = User.query.all()
            self.assertEqual(len(users), 1)

            story = db.session.query(Story).filter_by(id=1).first()
            self.assertNotEqual(story, None)

            # logout
            reply = logout(client)
            self.assertEqual(reply.status_code, 200)

            # signup
            user1 = User()
            user1.firstname = "Mario"
            user1.lastname = "Rossi"
            user1.email = "mario.rossi@gmail.com"
            user1.dateofbirth = "1994"
            user1.password = user1.set_password("12345")
            reply = signup(client, user1)
            self.assertEqual(reply.status_code, 200)

            users = User.query.all()
            self.assertEqual(len(users), 2)

            story = db.session.query(Story).filter_by(id=1).first()
            self.assertNotEqual(story, None)

            stories = Story.query.filter_by(id=1).all()
            self.assertEqual(len(stories), 1)

            reactions = Reaction.query.filter_by(story_id=1).all()
            self.assertEqual(len(reactions), 1)

            story = db.session.query(Story).filter_by(id=1).first()
            self.assertNotEqual(story, None)

            reactions = Reaction.query.filter_by(story_id=1).all()
            self.assertEqual(len(reactions), 1)

            # add reaction to a story
            reply = client.get('/stories/reaction/1/1')
            self.assertEqual(reply.status_code, 200)

            # logout
            reply = logout(client)
            self.assertEqual(reply.status_code, 200)

            # login
            reply = login(client, 'example@example.com', 'admin')
            self.assertEqual(reply.status_code, 200)

            story = db.session.query(Story).filter_by(id=1).first()
            self.assertNotEqual(story, None)

            reactions = Reaction.query.filter_by(story_id=1).all()
            self.assertEqual(len(reactions), 2)

            reply = client.post('stories/1/remove/index', follow_redirects=True)
            self.assertEqual(reply.status_code, 200)

            story = db.session.query(Story).filter_by(id=1).first()
            self.assertEqual(story, None)

            # logout
            reply = logout(client)
            self.assertEqual(reply.status_code, 200)

    def test_delete_wrong_author_story_index(self):

        global _app
        if _app is None:
            tested_app = create_app(debug=True)
            _app = tested_app
        else:
            tested_app = _app
        restart_db_tables(db, tested_app)

        with tested_app.test_client() as client:

            # login
            reply = login(client, 'example@example.com', 'admin')
            self.assertEqual(reply.status_code, 200)

            # add reaction to a story
            reply = client.get('/stories/reaction/1/1')
            self.assertEqual(reply.status_code, 200)

            users = User.query.all()
            self.assertEqual(len(users), 1)

            story = db.session.query(Story).filter_by(id=1).first()
            self.assertNotEqual(story, None)

            # logout
            reply = logout(client)
            self.assertEqual(reply.status_code, 200)

            # signup
            user1 = User()
            user1.firstname = "Mario"
            user1.lastname = "Rossi"
            user1.email = "mario.rossi@gmail.com"
            user1.dateofbirth = "1994"
            user1.password = user1.set_password("12345")
            reply = signup(client, user1)
            self.assertEqual(reply.status_code, 200)

            users = User.query.all()
            self.assertEqual(len(users), 2)

            story = db.session.query(Story).filter_by(id=1).first()
            self.assertNotEqual(story, None)

            stories = Story.query.filter_by(id=1).all()
            self.assertEqual(len(stories), 1)

            reactions = Reaction.query.filter_by(story_id=1).all()
            self.assertEqual(len(reactions), 1)

            story = db.session.query(Story).filter_by(id=1).first()
            self.assertNotEqual(story, None)

            reactions = Reaction.query.filter_by(story_id=1).all()
            self.assertEqual(len(reactions), 1)

            # add reaction to a story
            reply = client.get('/stories/reaction/1/1')
            self.assertEqual(reply.status_code, 200)

            reply = client.post('stories/1/remove/index', follow_redirects=True)
            self.assertEqual(reply.status_code, 200)

            story = db.session.query(Story).filter_by(id=1).first()
            self.assertNotEqual(story, None)

            # logout
            reply = logout(client)
            self.assertEqual(reply.status_code, 200)


if __name__ == '__main__':
    unittest.main()


def signup(client, user: User):
    return client.post('/signup', data=dict(
        firstname=user.firstname,
        lastname=user.lastname,
        email=user.email,
        dateofbirth=user.dateofbirth,
        password=user.password
    ), follow_redirects=True)