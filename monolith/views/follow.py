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
	# return OK


# Unfollow a writer
@follow.route('/follow/<userid>', methods=['DELETE'])
@login_required
def _unfollow_user(userid):
	#get the user who want to unfollow userid

	#if user not followed
	# rise notFollowedException

	# remove from follower_table the tuple (follower_id, followed_id)
	#return OK


# TODO: add to the API doc
# Show the follower list
@follow.route('/followers')
def followers():
    # followers = get_followers()
    # return render_template("users.html", users=followers)

# TODO: add to the API doc
# Show the follower list
@follow.route('/followed')
def followed():
    # followed = get_followed()
    # return render_template("users.html", users=followed)


# =============================================================================
# UTILITY FUNC
# =============================================================================

# Get the list of followers of the user_id
def get_followers(user_id):
	return []

# Get the list of users who follows the user_id
def get_followed(user_id):
	return []

# =============================================================================
# Exceptions
# =============================================================================


# =============================================================================
# TEST
# =============================================================================

import unittest
 
class TestFollow(unittest.TestCase):
 
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


    
 
 
if __name__ == '__main__':
    unittest.main()