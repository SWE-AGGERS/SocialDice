# =============================================================================
# TEST
# =============================================================================

import unittest
import json
from flask import request, jsonify
from monolith.app import create_app
from monolith.database import db, User, Followers
from monolith.follow import (
    _get_followers_of,
    _get_followed_by,
    _get_followers_number,
    _get_followed_number,
    _is_follower,
    _create_follow,
    _add_follow,
    _delete_follow
    )
 
class TestFollowFunction(unittest.TestCase):
 
    def test_get_followers_of(self):
        app = create_app()
        
        # push in the followers_table tuples
        item_1 = Followers()
        item_1.follower_id = 1
        item_1.followed_id = 2
        db.session.add(item_1)
        db.session.commit()

        item_2 = Follower()
        item_2.follower_id = 3
        item_2.followed_id = 2
        db.sesssion.add(item_2)
        db.session.commit()

        # call get_followers
        followers_1 = _get_followers_of(2)
        followers_2 = _get_followers_of(1)

        # assert correct 1
        self.assertEqual(followers_1, [1,3])

        # assert empty
        self.assertEqual(followers_2, [])
        # delete tuples
        db.session.delete(item_1)
        db.session.delete(item_2)
        db.session.commit()


    def test_get_followed_by(self):
        # push in the followers_table tuples
        item_1 = Followers()
        item_1.follower_id = 1
        item_1.followed_id = 2
        db.session.add(item_1)
        db.session.commit()

        item_2 = Followers()
        item_2.follower_id = 1
        item_2.follower_id = 3
        db.sesssion.add(item_2)
        db.session.commit()

        # call get_followed
        followed_1 = _get_followed_by(1)
        followed_2 = _get_followed_by(2)
        # assert correct 1
        self.assertEqual(followed_1, [2,3])

        # assert empty
        self.assertEqual(followed_2, [])

        # delete tuples
        db.session.delete(item_1)
        db.session.commit()
        db.session.delete(item_2)
        db.session.commit()

    def test_followers_number(self):
        # push in the followers_table tuples
        item_1 = Followers()
        item_1.follower_id = 1
        item_1.followed_id = 2
        db.session.add(item_1)
        db.session.commit()

        item_2 = Followers()
        item_2.follower_id = 3
        item_2.follower_id = 2
        db.sesssion.add(item_2)
        db.session.commit()

        # call get_followers
        followers_1 = _get_followers_number(2)
        followers_2 = _get_followers_number(1)

        # assert correct 1
        self.assertEqual(followers_1, 2)

        # assert empty
        self.assertEqual(followers_2, 0)
        # delete tuples
        db.session.delete(item_1)
        db.session.delete(item_2)
        db.session.commit()

    def test_followed_number(self):
        # push in the followers_table tuples
        item_1 = Followers()
        item_1.follower_id = 1
        item_1.followed_id = 2
        db.session.add(item_1)
        db.session.commit()

        item_2 = Followers()
        item_2.follower_id = 1
        item_2.follower_id = 3
        db.sesssion.add(item_2)
        db.session.commit()

        item_3 = Followers()
        item_3.follower_id = 3
        item_3.follower_id = 2
        db.sesssion.add(item_3)
        db.session.commit()

        # call get_followed
        followed_1 = _get_followed_number(1)
        followed_2 = _get_followed_number(2)

        # assert correct 1
        self.assertEqual(followed_1, 2)

        # assert empty
        self.assertEqual(followed_2, 0)

        # delete tuples
        db.session.delete(item_1)
        db.session.delete(item_2)
        db.session.delete(item_3)
        db.session.commit()


    def test_is_follower(self):
        # push in the followers_table (id_1, id_2)
        item_1 = Followers()
        item_1.follower_id = 1
        item_1.follower_id = 2
        db.session.add(item_1)
        
        # _is_follower(id_1, id_1)
        self.assertFalse(_is_follower(1,1))

        # _is_follower(id_1, id_2)
        self.assertTrue(_is_follower(1,2))

        # _is_follower(id_2, id_1)
        self.assertFalse(_is_follower(2,1))

        # _is_follower(id_1, id_3)
        self.assertFalse(_is_follower(1,3))

        # _is_follower(id_3, id_1)
        self.assertFalse(_is_follower(3,1))

        # _is_follower(id_3, id_4)
        self.assertFalse(_is_follower(4,5))



if __name__ == '__main__':
    unittest.main()