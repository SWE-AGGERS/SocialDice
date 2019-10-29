import unittest
import json
from flask import request, jsonify
from monolith.app import create_app
from monolith.database import db, User

 
class TestFollow(unittest.TestCase):

    def test_follow_user(self):
        tested_app = create_app(debug=True)
        with tested_app.test_client() as client:
            with client.session_transaction() as sess:
                # push in the users_table 3 users
                user_a = User()
                user_a.email = 'testa@test.com'
                user_a.set_password('test')

                user_b = User()
                user_b.email = 'testb@test.com'
                user_b.set_password('test')

                user_c = User()
                user_c.email = 'testc@test.com'
                user_c.set_password ('test')

                db.session.add(user_a)
                db.session.add(user_b)
                db.session.add(user_c)
                db.session.commit()

                # Get users ID
                user_a_id = User.query.filter_by(email=user_a.email).first().get_id()
                user_b_id = User.query.filter_by(email=user_b.email).first().get_id()
                user_c_id = User.query.filter_by(email=user_c.email).first().get_id()
            
            # login as user_1
            login(client, 'testa@test.com', 'test')

            # call /follow/user_id_2

            reply = client.post('/follow/3')
            print(">>>>>>>>>>>>>>>>>\nREPLY:")
            print(reply)
            print("USERB ID: ")
            print(user_b_id)
            print(">>>>>>>>>>>>>>>>>>>>>>>>")

            # assert OK
            self.assertEqual({"follower":1}, reply)

            # call /follow/user_id_2
            # assert EXC

            # call /follow/user_id_3
            # assert OK

            # call /follow/user_id_2
            # assert EXC

            # call /follow/user_id_1 (himslef)
            # assert EXC

            # call /follow/user_not_exist
            # assert EXC
            
            # delete users and followers

    def test_unfollow_user(self):
        # TODO
        # push in the user_table 3 users
        # push follows in follow_table (1-2, 1-3, 2-3)
        # create correct_answers
        # login as user_1

        # call /unfollow/user_1
        # assert EXC

        # call /unfollow/user_2
        # assert OK

        # call unfollow/user_2
        # assert EXC

        # call unfollow/user_not_exist
        # assert EXC
        assert True


# TO DELETE MAYBE?
def login(client, username, password):
    return client.post('/login', data=dict(
        email=username,
        password=password
    ), follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)