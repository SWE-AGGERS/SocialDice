from flask import Blueprint, redirect, render_template, request, jsonify
from monolith.database import db, User, Followers
from monolith.forms import UserForm
from monolith.app import create_app as app
from flask_login import current_user, login_required

follow = Blueprint('follow', __name__)

# Follow a writer
@follow.route('/follow/<int:userid>', methods=['POST'])
@login_required
def _follow_user(userid):
    # get the user who want following userid
    subject = current_user.id


    # if user already followed
    if userid == subject:
        return jsonify({"followed": -1})

    # add to follower_table the tuple (follower_id, followed_id)
    _add_follow(subject, userid)

    # return OK + number of users followed
    return jsonify({"followed": _get_followed_number(subject)})


# Unfollow a writer
@follow.route('/follow/<int:userid>', methods=['DELETE'])
@login_required
def _unfollow_user(userid):
    #get the user who want to unfollow userid
    subject = current_user.id

    if userid == subject:
        jsonify({"followed": -1})

    # if user not followed
    if not _is_follower(subject, userid):
        jsonify({"followed": -1})

    # remove from follower_table the tuple (follower_id, followed_id)
    _delete_follow(subject, userid)

    # return OK + number of users followed
    return jsonify({"followed": _get_followed_number(subject)})

# TODO: add to the API doc
# return the followers list
@follow.route('/followers/list', methods=['GET'])
@login_required
def _followers_list():
    subject = current_user.id
    return jsonify({"followers": get_followers(subject)})

# TODO: add to the API doc
# Return the followed list
@follow.route('/followed/list', methods=['GET'])
@login_required
def _followed_list():
    subject = current_user.id
    return jsonify({"followed": get_followed(subject)})



# TODO: add to API doc
# return number of followers
@follow.route('/followers', methods=['GET'])
@login_required
def _followers_numer():
    # return json with OK, and the number
    return jsonify({"followers": _get_followers_number(current_user.id)})


# TODO: add to API doc
# return number of followers
@follow.route('/followed', methods=['GET'])
@login_required
def _followed_numer():
    # return json with OK, and the number
    return jsonify({"followed": _get_followed_number(current_user.id)})




# =============================================================================
# UTILITY FUNC
# =============================================================================

# Get the list of followers of the user_id
def _get_followers_of(user_id):
    L = Followers.query.filter_by(follower_id=user_id).all()
    return L

# Get the list of users who follows the user_id
def _get_followed_by(user_id):
    L = Followers.query.filter_by(followed_id=user_id).all()
    return L


# Get the number of followers
def _get_followers_number(user_id):
    return size(_get_followers_of(user_id))


# Get the number of followed
def _get_followed_number(user_id):
    return size(_get_followed_by(user_id))

# check if user_a follow user_b
def _is_follower(user_a, user_b):
    """check if user_a follow user_b"""
    item = Followers.query.filter_by(follower_id=user_a, followed_id=user_b).first()
    if item is None:
        return False
    else:
        return True


def _create_follow(user_a, user_b):
    item = Follower()
    item.follower_id = user_a
    item.followed_id = user_b
    return item


# TODO: use celerity
def _add_follow(user_a, user_b):
    db.session.add(_create_follow(user_a, user_b))
    db.session.commit()


# TODO: use celerity
def _delete_follow(user_a, user_b):
    db.session.delete(_create_follow(user_a, user_b))
    db.session.commit()
# =============================================================================
# TEST
# =============================================================================

import unittest
 
class TestFollowFunction(unittest.TestCase):
 
    def test_get_followers_of(self):
        from monolith.database import db, Followers
        from monolith.app import create_app as app
        
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