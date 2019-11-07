import unittest

from monolith.app import create_app
from monolith.background import update_reactions
from monolith.database import db, Story, Reaction
from monolith.database import User
from monolith.views.stories import add_reaction

_app = None


class TestReactionCounters(unittest.TestCase):
    def test1(self):
        global _app
        tested_app = create_app(debug=True)
        _app = tested_app
        with tested_app.test_client() as client:
            with client.session_transaction() as sess:
                db.drop_all()
                db.create_all()

                # create user
                user_a = User()
                user_a.email = 'testa@test.com'
                user_a.set_password('test')
                db.session.add(user_a)
                db.session.commit()

                user_b = User()
                user_b.email = 'testb@test.com'
                user_b.set_password('test')
                db.session.add(user_b)
                db.session.commit()

                # create story
                story = Story()
                story.text = 'Text a'
                story.likes = 0
                story.dislikes = 0
                story.author_id = user_a.get_id()
                story.roll = {'dice': ['bike', 'tulip', 'happy', 'cat', 'ladder', 'rain']}
                db.session.add(story)
                db.session.commit()

                # add like
                like = Reaction()
                like.marked = 0
                like.story_id = story.id
                like.user_id = user_b.id
                like.type = 1
                db.session.add(story)
                db.session.commit()

                # create 1000 user and like the story
                users = []
                for i in range(10):
                    user = User()
                    user.email = 'user' + str(i) + '@test.com'
                    user.set_password('test')
                    db.session.add(user)
                    users.append(user)
                    db.session.add(story)

                db.session.commit()
                for u in users:
                    add_reaction(u.id, 1, 1)
                #
                # reaction = Reaction.query.count()
                # print(str(reaction)))
                res = update_reactions.apply_async(args=[1],  time_limit=3)
                res.get()
                q = Story.query.filter_by(author_id=1).first()
                self.assertEqual(int(q.likes), 10)


