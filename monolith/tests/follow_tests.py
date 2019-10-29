import unittest
import json
from flask import request, jsonify
from monolith.app import create_app

 
class TestFollow(unittest.TestCase):

    def test_follow_user(self):
        tested_app = create_app(debug=True)
        with tested_app.test_client() as client:
            # push in the users_table 3 users
            user_a = User()
            user_a.email = 'testa@test.com'
            user_a.setpassword('test')
            user_a_id = user_a.getId()

            user_b = User()
            user_b.email = 'testb@test.com'
            user_b.setpassword('test')
            user_b_id = user_a.getId()

            user_c = User()
            user_c.email = 'testc@test.com'
            user_c.setpassword ('test')
            user_c_id = user_a.getId()

            db.session.add(user_a)
            db.session.add(user_b)
            db.session.add(user_c)
            db.session.commit()

            # create correct_answers
            # login as user_1
            login(client, 'testa@test.com', 'test')

            # call /follow/user_id_2
            reply = client.post('/follow/'+user_b_id)
            # assert OK
            assert {'followed': 1} == reply

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