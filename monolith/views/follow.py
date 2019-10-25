from flask import Blueprint, redirect, render_template, request
from monolith.database import db, User
from monolith.auth import admin_required
from monolith.forms import UserForm
from flask_login import (current_user, login_user, logout_user,
                         login_required)

follow = Blueprint('follow', __name__)

# Follow a writer
@follow.route('/follow/<userid>', methods=['POST'])
@login_required
def _follow_user(userid):
	# get the user who want followng userid
	subject = current_user.id


	# if user already followed
	# rise alreadyFollowedException

	# add to follower_table the tuple (follower_id, followed_id)
	# return OK + number of followers


# Unfollow a writer
@follow.route('/follow/<userid>', methods=['DELETE'])
@login_required
def _unfollow_user(userid):
	#get the user who want to unfollow userid

	#if user not followed
	# rise notFollowedException

	# remove from follower_table the tuple (follower_id, followed_id)
	#return OK + number of followers


# TODO: add to the API doc
# return the followers list
@follow.route('/followers/list')
@login_required
def _followers_list():
    # followers = get_followers()
    # return json Ok, followers

# TODO: add to the API doc
# Return the followed list
@follow.route('/followed/list')
@login_required
def _followed_list():
    # followed = get_followed()
    # return json OK, followed


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
	return []


# Get the list of users who follows the user_id
def _get_followed(user_id):
	return []


# Get the number of followers
def _get_followers_number(user_id):
	return size(_get_followers(user_id))


# Get the number of followed
def _get_followed_number(user_id):
	return size(_get_followed(user_id))
# =============================================================================
# Exceptions
# =============================================================================


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

if __name__ == '__main__':
    unittest.main()