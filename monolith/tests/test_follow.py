import unittest
import json
from flask import request, jsonify
from monolith.app import create_app
from monolith.database import db, User, Followers
from monolith.auth import login_manager
from monolith.views.follow import _create_follow, _is_follower
from monolith.tests.restart_db import restart_db_tables


_app = None
 
class TestFollow(unittest.TestCase):

    def test_follow_user(self):
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

                db.session.add(user_a)
                db.session.add(user_b)
                db.session.add(user_c)
                db.session.commit()

                # Get users ID
                user_a_id = User.query.filter_by(email=user_a.email).first().get_id()
                user_b_id = User.query.filter_by(email=user_b.email).first().get_id()
                user_c_id = User.query.filter_by(email=user_c.email).first().get_id()
            
            # login as user_1
            login(client, user_a.email, 'test')

            # call /follow/user_id_2
            # assert True, redirtect to user_2 wall 
            reply = client.post('/follow/'+str(user_b_id))
            data = "/wall/"+str(user_b_id)
            self.assertTrue(_is_follower(user_a_id, user_b_id))
            self.assertIn(data, str(reply.data))

            # call /follow/user_id_2
            # assert True, redirtect to user_2 wall
            data = "/wall/"+str(user_b_id)
            reply = client.post('/follow/'+str(user_b_id))
            self.assertTrue(_is_follower(user_a_id, user_b_id))
            self.assertIn(data, str(reply.data))

            # call /follow/user_id_3
            # assert True, redirtect to user_3 wall
            data = "/wall/"+str(user_c_id)
            reply = client.post('/follow/'+str(user_c_id))
            self.assertTrue(_is_follower(user_a_id, user_c_id))
            self.assertIn(data, str(reply.data))

            # call /follow/user_id_2
            # assert True, redirect to user_2 wall
            data = "/wall/"+str(user_b_id)
            reply = client.post('/follow/'+str(user_b_id))
            self.assertTrue(_is_follower(user_a_id, user_b_id))
            self.assertIn(data, str(reply.data))

            # call /follow/user_id_1 (himslef)
            # assert False, redirect to user_1 wall
            data = "/wall/"+str(user_a_id)
            reply = client.post('/follow/'+str(user_a_id))  
            self.assertFalse(_is_follower(user_a_id, user_a_id))
            self.assertIn(data, str(reply.data))

            # call /follow/user_not_exist
            # assert False, redirect to stories
            user_not_exist_id = 99999999999
            reply = client.post('/follow/'+str(user_not_exist_id))
            self.assertFalse(_is_follower(user_a_id, user_not_exist_id))
            self.assertIn("/stories", str(reply.data))
            logout(client)        

    def test_followers_list(self):
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
                    user_a.firstname = "Pippo"
                    user_a.lastname = "Pippo"
                    user_a.email = 'testa@test.com'
                    user_a.set_password('test')

                    user_b = User()
                    user_b.firstname = "Pluto"
                    user_b.lastname = "Mouse"
                    user_b.email = 'testb@test.com'
                    user_b.set_password('test')

                    user_c = User()
                    user_c.email = 'testc@test.com'
                    user_c.set_password('test')

                    db.session.add(user_a)
                    db.session.add(user_b)
                    db.session.add(user_c)
                    db.session.commit()

                    # Get users ID
                    user_a_id = User.query.filter_by(email=user_a.email).first().get_id()
                    user_b_id = User.query.filter_by(email=user_b.email).first().get_id()

                
                # login as user_1
                login(client, user_a.email, 'test')

                # call /follow/user_id_2
                # assert True, redirtect to user_2 wall 
                reply = client.post('/follow/'+str(user_b_id))
                data = "/wall/"+str(user_b_id)
                self.assertTrue(_is_follower(user_a_id, user_b_id))
                self.assertIn(data, str(reply.data))

                # get followed list
                reply = client.get("/followed/list")
                self.assertIn(user_b.firstname, str(reply.data))

                # get followed number
                reply = client.get("/followed")
                assert b'"followed_num":1' in reply.data

                # logout user1
                logout(client)

                # login as user2
                login(client, user_b.email, 'test')

                # get followers list
                reply = client.get("/followers/list")
                self.assertIn(user_a.firstname, str(reply.data))

                # get followers number
                reply = client.get("/followers")
                assert b'"followers_num":1' in reply.data
                    

    def test_unfollow_user(self):

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

                db.session.add(user_a)
                db.session.add(user_b)
                db.session.add(user_c)
                db.session.commit()

                # Get users ID
                user_a_id = User.query.filter_by(email=user_a.email).first().get_id()
                user_b_id = User.query.filter_by(email=user_b.email).first().get_id()
                user_c_id = User.query.filter_by(email=user_c.email).first().get_id()

            with client.session_transaction() as session:
                follow_ab = _create_follow(user_a_id, user_b_id)
                follow_ac = _create_follow(user_a_id, user_c_id)
                follow_bc = _create_follow(user_b_id, user_c_id)

                db.session.add(follow_ab)
                db.session.add(follow_ac)
                db.session.add(follow_bc)
                db.session.commit()

            # login as user_1
            login(client, user_a.email, 'test')


            # call /unfollow/user_1
            # assert False
            data = '/wall/'+str(user_a_id)
            reply = client.delete('/follow/'+str(user_a_id))
            self.assertFalse(_is_follower(user_a_id, user_a_id))
            self.assertIn(data, str(reply.data))

            # call /unfollow/user_2
            # assert OK
            data = '/wall/'+str(user_b_id)
            self.assertTrue(_is_follower(user_a_id, user_b_id))
            reply = client.delete('/follow/'+str(user_b_id))
            self.assertFalse(_is_follower(user_a_id, user_b_id))
            self.assertIn(data, str(reply.data))

            # call unfollow/user_2
            # assert EXC
            data = '/wall/'+str(user_b_id)
            reply = client.delete('/follow/'+str(user_b_id))
            self.assertFalse(_is_follower(user_a_id, user_b_id))
            self.assertIn(data, str(reply.data))

            # call unfollow/user_not_exist
            # assert EXC
            user_not_exist_id = 999999999999
            data = '/wall/'+str(user_not_exist_id)
            reply = client.delete('/follow/'+str(user_not_exist_id))
            self.assertFalse(_is_follower(user_a_id, user_not_exist_id))
            self.assertIn("/stories", str(reply.data))
            logout(client)


    def test_unfollow_post_user(self):

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

                db.session.add(user_a)
                db.session.add(user_b)
                db.session.add(user_c)
                db.session.commit()

                # Get users ID
                user_a_id = User.query.filter_by(email=user_a.email).first().get_id()
                user_b_id = User.query.filter_by(email=user_b.email).first().get_id()
                user_c_id = User.query.filter_by(email=user_c.email).first().get_id()

            with client.session_transaction() as session:
                follow_ab = _create_follow(user_a_id, user_b_id)
                follow_ac = _create_follow(user_a_id, user_c_id)
                follow_bc = _create_follow(user_b_id, user_c_id)

                db.session.add(follow_ab)
                db.session.add(follow_ac)
                db.session.add(follow_bc)
                db.session.commit()

            # login as user_1
            login(client, user_a.email, 'test')


            # call /unfollow/user_1
            # assert False
            data = '/wall/'+str(user_a_id)
            reply = client.post('/unfollow/'+str(user_a_id))
            self.assertFalse(_is_follower(user_a_id, user_a_id))
            self.assertIn(data, str(reply.data))

            # call /unfollow/user_2
            # assert OK
            data = '/wall/'+str(user_b_id)
            self.assertTrue(_is_follower(user_a_id, user_b_id))
            reply = client.post('/unfollow/'+str(user_b_id))
            self.assertFalse(_is_follower(user_a_id, user_b_id))
            self.assertIn(data, str(reply.data))

            # call unfollow/user_2
            # assert EXC
            data = '/wall/'+str(user_b_id)
            reply = client.post('/unfollow/'+str(user_b_id))
            self.assertFalse(_is_follower(user_a_id, user_b_id))
            self.assertIn(data, str(reply.data))

            # call unfollow/user_not_exist
            # assert EXC
            user_not_exist_id = 999999999999
            data = '/wall/'+str(user_not_exist_id)
            reply = client.post('/unfollow/'+str(user_not_exist_id))
            self.assertFalse(_is_follower(user_a_id, user_not_exist_id))
            self.assertIn("/stories", str(reply.data))
            logout(client)

# TO DELETE MAYBE?
def login(client, username, password):
    return client.post('/login', data=dict(
        email=username,
        password=password
    ), follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)

if __name__ == '__main__':
    unittest.main()