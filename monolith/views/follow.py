from flask import Blueprint, redirect, render_template, request, jsonify
from monolith.database import db, User
from monolith.forms import UserForm
from flask_login import current_user, login_required 

follow = Blueprint('follow', __name__)

# Follow a writer
@follow.route('/follow/<int:userid>', methods=['POST'])
@login_required
def _follow_user(userid):
	# get the user who want followng userid
	subject = current_user.id


	# if user already followed
    if userid == subject:
       # TODO: Gestire

	# add to follower_table the tuple (follower_id, followed_id)
    # TODO
	# return OK + number of followed
    return jsonify({"followed": _get_followed_number(subject)})


# Unfollow a writer
@follow.route('/follow/<int:userid>', methods=['DELETE'])
@login_required
def _unfollow_user(userid):
	#get the user who want to unfollow userid
    subject = current_user.id

    if userid == subject:
        # TODO: Gestire

	# if user not followed
    if not _is_follower(subject, userid):
        # TODO: Gestire

	# remove from follower_table the tuple (follower_id, followed_id)
    # TODO
	# return OK + number of followers
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


# TODO: add to API doc
# return number of followers
@follow.route('/followed', methods=['GET'])
@login_required
def _followed_numer():
	# return json with OK, and the number



# =============================================================================
# UTILITY FUNC
# =============================================================================

# Get the list of followers of the user_id
def _get_followers(user_id):
    # TODO
	return []


# Get the list of users who follows the user_id
def _get_followed(user_id):
    # TODO
	return []


# Get the number of followers
def _get_followers_number(user_id):
	return size(_get_followers(user_id))


# Get the number of followed
def _get_followed_number(user_id):
	return size(_get_followed(user_id))

# check if user_a follow user_b
def _is_follower()
    """check if user_a follow user_b"""
    # TODO
    return False
# =============================================================================
# TEST
# =============================================================================

import unittest
 
class TestFollowFunction(unittest.TestCase):
 
    def test_get_followers(self):
        # push in the followers_table tuples
        # create correct_answer
        # call get_followers
        # assert correct 1
        # assert correct 2
        # assert empty
        # delete tuples


    def test_get_followed(self):
    	# push in the followers_table tuples
        # create correct_answer
        # call get_followers
        # assert correct 1
        # assert correct 2
        # assert empty
        # delete tuples

    def test_followers_number(self):
    	# TODO

    def test_followed_number(self):
    	# TODO

    def test_is_follower(self):
        # push in the followers_table (id_1, id_2)
        
        # _is_follower(id_1, id_1)
        # assert fail

        # _is_follower(id_1, id_2)
        # assert OK

        # _is_follower(id_2, id_1)
        # assert fail

        # _is_follower(id_1, id_3)
        # assert fail

        # _is_follower(id_3, id_1)
        # assert fail

        # _is_follower(id_3, id_4)
        # assert fail



if __name__ == '__main__':
    unittest.main()