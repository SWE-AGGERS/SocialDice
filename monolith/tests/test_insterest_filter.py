import unittest
from monolith.views.follow import _create_follow
from monolith.interest_filter import get_limit_stories
from monolith.database import Story, db, User, Followers
from monolith.app import create_app
from monolith.tests.restart_db import restart_db_tables

_app = None
 
class TestInterest(unittest.TestCase):

    def test_interest_filter(self):
        global _app
        if _app is None:
            tested_app = create_app(debug=True)
            _app = tested_app
        else:
            tested_app = _app
        restart_db_tables(db, tested_app)

        # Create 9 users
        # Create 3 story for user
        # Create a follow between 2 users 
        # (every user N follow each others except himself and N+1)

        with tested_app.test_client() as client:
            with client.session_transaction() as session:
                for i in range(1, 10):
                    tmp = User()
                    tmp.email = "a"+str(i)+"@example.it"
                    tmp.firstname =  str(i)
                    tmp.lastname = str(i)+"lastname"
                    tmp.set_password("abcd1234")
                    db.session.add(tmp)
                db.session.commit()
            with client.session_transaction() as session:
                for i in range(1, 30):
                    tmp = make_story((1+i)%10+1)
                    db.session.add(tmp)
                db.session.commit()
            with client.session_transaction() as session:
                for i in range(1,10):
                    for j in range(1,10):
                        if i != j and i != j-1:
                            tmp = _create_follow(i+1, j+1)
                            db.session.add(tmp)
                db.session.commit()

            login(client, "a1@example.it", "abcd1234")
            with client.session_transaction() as session:
                # 21 stories
                storylist = get_limit_stories(user_id=2, max_size_random=0)
                print(len(storylist))
        self.assertEqual(len(storylist), 21)

        with tested_app.test_client() as client:
            with client.session_transaction() as session:
                # 23 stories
                storylist = get_limit_stories(user_id=2)#, max_size_random=2)
                print(len(storylist))
        self.assertEqual(len(storylist), 23)






# Return a story object
def make_story(userid, text="test text", likes=0, dislikes=0):
    example = Story()
    example.text = text
    example.likes = likes
    example.dislikes = dislikes
    example.author_id = userid
    return example

def login(client, username, password):
    return client.post('/login', data=dict(
        email=username,
        password=password
    ), follow_redirects=True)


