import unittest
import json
from flask import request, jsonify
from monolith.app import create_app
from monolith.database import db, User, Followers
from monolith.auth import login_manager
from monolith.views.follow import _create_follow
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
            reply = client.post('/follow/'+str(user_b_id))

            # assert OK
            self.assertIn(b'{"followed":1}', reply.data)

            # call /follow/user_id_2
            # assert EXC
            reply = client.post('/follow/'+str(user_b_id))
            self.assertIn(b'{"followed":-1}', reply.data)

            # call /follow/user_id_3
            # assert OK
            reply = client.post('/follow/'+str(user_c_id))
            self.assertIn(b'{"followed":2}', reply.data)

            # call /follow/user_id_2
            # assert EXC
            reply = client.post('/follow/'+str(user_b_id))
            self.assertIn(b'{"followed":-1}', reply.data)

            # call /follow/user_id_1 (himslef)
            # assert EXC
            reply = client.post('/follow/'+str(user_a_id))  
            self.assertIn(b'{"followed":-1}', reply.data)

            # call /follow/user_not_exist
            # assert EXC
            reply = client.post('/follow/'+str(-999))  
            self.assertIn(b'{"followed":-1}', reply.data)
            logout(client)        
                          

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
            # assert EXC
            reply = client.delete('/follow/'+str(user_a_id))
            self.assertIn(b'"followed":-1', reply.data)

            # call /unfollow/user_2
            # assert OK
            reply = client.delete('/follow/'+str(user_b_id))
            self.assertIn(b'"followed":1', reply.data)

            # call unfollow/user_2
            # assert EXC
            reply = client.delete('/follow/'+str(user_b_id))
            self.assertIn(b'"followed":-1', reply.data)

            # call unfollow/user_not_exist
            # assert EXC
            reply = client.delete('/follow/'+str(999))
            self.assertIn(b'"followed":-1', reply.data)

            logout(client)



# TO DELETE MAYBE?
def login(client, username, password):
    return client.post('/login', data=dict(
        email=username,
        password=password
    ), follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)