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
