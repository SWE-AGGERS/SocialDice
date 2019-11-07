import unittest
from monolith.database import db, User, Followers, Story
from monolith.tests.restart_db import restart_db_tables
from monolith.app import create_app
from monolith.background import *
from monolith.views.follow import _create_follow

_app = None
 
class TestEmail(unittest.TestCase):

    def test_send_email(self):
        global _app
        if _app is None:
            tested_app = create_app(debug=True)
            _app = tested_app
        else:
            tested_app = _app
        restart_db_tables(db, tested_app)


    def test_getuser(self):
        global _app
        if _app is None:
            tested_app = create_app(debug=True)
            _app = tested_app
        else:
            tested_app = _app
        restart_db_tables(db, tested_app)

        with tested_app.test_client() as client:
            with client.session_transaction() as session:
                user_base = User.query.first()
                # push in the users_table 3 users
                user_a = User()
                user_a.email = 'testa@test.com'
                user_a.set_password('test')

                user_b = User()
                user_b.email = 'testb@test.com'
                user_b.set_password('test')

                user_c = User()
                user_c.email = 'testc@test.com'
                user_c.set_password('test')

                db.session.add(user_a)
                db.session.add(user_b)
                db.session.add(user_c)
                db.session.commit()
                res = get_users()
        correct = [user_base, user_a, user_b, user_c]
        print(res)
        print(correct)
        self.assertEqual(res, correct)


    def test_maker_message(self):
        global _app
        if _app is None:
            tested_app = create_app(debug=True)
            _app = tested_app
        else:
            tested_app = _app
        restart_db_tables(db, tested_app)

        with tested_app.test_client() as client:
            with client.session_transaction() as session:
                # push in the users_table 3 users
                user_a = User()
                user_a.firstname = 'user_a'
                user_a.email = 'testa@test.com'
                user_a.set_password('test')

                user_b = User()
                user_b.firstname = 'user_b'
                user_b.lastname = 'surname_b'
                user_b.email = 'testb@test.com'
                user_b.set_password('test')

                user_c = User()
                user_c.firstname = 'user_c'
                user_c.lastname = 'surname_c'
                user_c.email = 'testc@test.com'
                user_c.set_password('test')

                user_d = User()
                user_d.firstname = 'user_d'
                user_d.lastname = 'surname_d'
                user_d.email = 'testd@test.com'
                user_d.set_password('test')

                db.session.add(user_a)
                db.session.add(user_b)
                db.session.add(user_c)
                db.session.add(user_d)
                db.session.commit()

                # Get users ID
                user_a_id = User.query.filter_by(email=user_a.email).first().get_id()
                user_b_id = User.query.filter_by(email=user_b.email).first().get_id()
                user_c_id = User.query.filter_by(email=user_c.email).first().get_id()
                user_d_id = User.query.filter_by(email=user_d.email).first().get_id()

            with client.session_transaction() as session:
                follow_ab = _create_follow(user_a_id, user_b_id)
                follow_ac = _create_follow(user_a_id, user_c_id)
                follow_ad = _create_follow(user_a_id, user_d_id)
                follow_bc = _create_follow(user_b_id, user_c_id)

                db.session.add(follow_ab)
                db.session.add(follow_ac)
                db.session.add(follow_ad)
                db.session.add(follow_bc)

                story_b_1 = make_story(user_b_id, "story_b_1")
                story_b_2 = make_story(user_b_id, "story_b_2")
                story_b_3 = make_story(user_b_id, "story_b_3", 66, 9)
                story_b_4 = make_story(user_b_id, "story_b_4", 5, 1)

                story_c_1 = make_story(user_c_id, "story_c_1")
                story_c_2 = make_story(user_c_id, "story_c_2", 1000, 162)
                story_c_3 = make_story(user_c_id, "story_c_3")

                db.session.add(story_b_1)
                db.session.add(story_b_2)
                db.session.add(story_b_3)
                db.session.add(story_b_4)

                db.session.add(story_c_1)
                db.session.add(story_c_2)
                db.session.add(story_c_3)

                db.session.commit()

                res = maker_message(user_a)
                print(res)
                correct = "Hello user_a,\n\nhere you can find what's new on the wall of Sweaggers' SocialDice!\n\n - user_b surname_b posts 4 new stories.\n - user_c surname_c posts 3 new stories.\n\nSee you on SocialDice,\nSweaggers Team"
                self.assertEqual(res, correct)

                res = maker_message(user_d)
                correct = "Hello user_d,\n\nYou have no news for today, take a look and add new writers on Sweaggers' SocialDice!"
                self.assertEqual(res, correct)

    def test_get_all_stories_by_writer(self):
        global _app
        if _app is None:
            tested_app = create_app(debug=True)
            _app = tested_app
        else:
            tested_app = _app
        restart_db_tables(db, tested_app)

        with tested_app.test_client() as client:
            with client.session_transaction() as session:
                # push in the users_table 3 users
                user_a = User()
                user_a.email = 'testa@test.com'
                user_a.set_password('test')

                user_b = User()
                user_b.email = 'testb@test.com'
                user_b.set_password('test')

                user_c = User()
                user_c.email = 'testc@test.com'
                user_c.set_password('test')

                user_d = User()
                user_d.email = 'testd@test.com'
                user_d.set_password('test')

                db.session.add(user_a)
                db.session.add(user_b)
                db.session.add(user_c)
                db.session.add(user_d)
                db.session.commit()

                # Get users ID
                user_a_id = User.query.filter_by(email=user_a.email).first().get_id()
                user_b_id = User.query.filter_by(email=user_b.email).first().get_id()
                user_c_id = User.query.filter_by(email=user_c.email).first().get_id()
                user_d_id = User.query.filter_by(email=user_d.email).first().get_id()

            with client.session_transaction() as session:
                follow_ab = _create_follow(user_a_id, user_b_id)
                follow_ac = _create_follow(user_a_id, user_c_id)
                follow_ad = _create_follow(user_a_id, user_d_id)
                follow_bc = _create_follow(user_b_id, user_c_id)

                db.session.add(follow_ab)
                db.session.add(follow_ac)
                db.session.add(follow_ad)
                db.session.add(follow_bc)

                story_b_1 = make_story(user_b_id, "story_b_1")
                story_b_2 = make_story(user_b_id, "story_b_2")
                story_b_3 = make_story(user_b_id, "story_b_3", 66, 9)
                story_b_4 = make_story(user_b_id, "story_b_4", 5, 1)

                story_c_1 = make_story(user_c_id, "story_c_1")
                story_c_2 = make_story(user_c_id, "story_c_2", 1000, 162)
                story_c_3 = make_story(user_c_id, "story_c_3")

                db.session.add(story_b_1)
                db.session.add(story_b_2)
                db.session.add(story_b_3)
                db.session.add(story_b_4)

                db.session.add(story_c_1)
                db.session.add(story_c_2)
                db.session.add(story_c_3)

                db.session.commit()

                res = get_all_stories_by_writer(user_b_id)
                self.assertEqual(len(res), 4)
                res = get_all_stories_by_writer(user_c_id)
                self.assertEqual(len(res), 3)
                res = get_all_stories_by_writer(user_d_id)
                self.assertEqual(len(res), 0)


    def test_get_followed_list(self):
        global _app
        if _app is None:
            tested_app = create_app(debug=True)
            _app = tested_app
        else:
            tested_app = _app
        restart_db_tables(db, tested_app)

        with tested_app.test_client() as client:
            with client.session_transaction() as session:
                # push in the users_table 3 users
                user_a = User()
                user_a.email = 'testa@test.com'
                user_a.set_password('test')

                user_b = User()
                user_b.email = 'testb@test.com'
                user_b.set_password('test')

                user_c = User()
                user_c.email = 'testc@test.com'
                user_c.set_password('test')

                user_d = User()
                user_d.email = 'testd@test.com'
                user_d.set_password('test')

                db.session.add(user_a)
                db.session.add(user_b)
                db.session.add(user_c)
                db.session.add(user_d)
                db.session.commit()

                # Get users ID
                user_a_id = User.query.filter_by(email=user_a.email).first().get_id()
                user_b_id = User.query.filter_by(email=user_b.email).first().get_id()
                user_c_id = User.query.filter_by(email=user_c.email).first().get_id()
                user_d_id = User.query.filter_by(email=user_d.email).first().get_id()

            with client.session_transaction() as session:
                follow_ab = _create_follow(user_a_id, user_b_id)
                follow_ac = _create_follow(user_a_id, user_c_id)
                follow_ad = _create_follow(user_a_id, user_d_id)
                follow_bc = _create_follow(user_b_id, user_c_id)

                db.session.add(follow_ab)
                db.session.add(follow_ac)
                db.session.add(follow_ad)
                db.session.add(follow_bc)
                db.session.commit()

                res = get_followed_list(user_a_id)
                correct = [user_b_id, user_c_id, user_d_id]
                self.assertEqual(res, correct)



# Return a story object
def make_story(userid, text="test text", likes=0, dislikes=0):
    example = Story()
    example.text = text
    example.likes = likes
    example.dislikes = dislikes
    example.author_id = userid
    return example