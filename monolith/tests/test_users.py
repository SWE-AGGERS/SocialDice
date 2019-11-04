import unittest

from monolith.app import create_app
from monolith.database import db, User, Story
from monolith.views.users import reduce_list
from sqlalchemy import desc


class UserTest(unittest.TestCase):

    def test_reduce_list(self):
        tested_app = create_app(debug=True)
        with tested_app.test_client() as client:
            with client.session_transaction():
                user_stories = db.session.query(User, Story) \
                    .join(Story) \
                    .order_by(desc(Story.id))

                user_stories = reduce_list(user_stories)

                users = db.session.query(User)

                for user in users:
                    filtered = list(filter(lambda x: x[0].id == user.id, user_stories))
                    print(user, filtered)
                    self.assertTrue(len(filtered) in [0, 1])
