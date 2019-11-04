from flask import Blueprint, jsonify, redirect
from monolith.database import db, Followers, User
from flask_login import current_user, login_required

follow = Blueprint('follow', __name__)

# Follow a writer
@follow.route('/follow/<int:userid>', methods=['POST'])
@login_required
def _follow_user(userid):
    # get the user who want following userid
    subject = current_user.id

    # if try to follow himeself
    if int(userid) == int(subject):
        return redirect('/wall/'+str(userid))

    # if already followed
    if _is_follower(subject, userid):
        return redirect('/wall/'+str(userid))

    # if the followed user do not exist
    if User.query.filter_by(id=userid).first() == None:
        return redirect('/stories')

    # add to follower_table the tuple (follower_id, followed_id)
    result = _add_follow(subject, userid)
    if result == -1:
        # db.session.add error
        return redirect('/stories')

    # return OK + number of users followed
    return redirect('/wall/'+str(userid))


# Unfollow a writer
@follow.route('/follow/<int:userid>', methods=['DELETE'])
@login_required
def _unfollow_user(userid):
    #get the user who want to unfollow userid
    subject = current_user.id

    if userid == subject:
        return jsonify({"followed": -1})

    # if user not followed
    if not _is_follower(subject, userid):
        return jsonify({"followed": -1})

    # remove from follower_table the tuple (follower_id, followed_id)
    if _delete_follow(subject, userid) == -1:
        # db delete error
        return jsonify({"followed": -1})


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
    return len(_get_followed_by(user_id))


# Get the number of followed
def _get_followed_number(user_id):
    return len(_get_followers_of(user_id))

# check if user_a follow user_b
def _is_follower(user_a, user_b):
    """check if user_a follow user_b"""
    item = Followers.query.filter_by(follower_id=user_a, followed_id=user_b).first()
    if item is None:
        return False
    else:
        return True


def _create_follow(user_a, user_b):
    item = Followers()
    item.follower_id = int(user_a)
    item.followed_id = int(user_b)
    return item


# TODO: use celerity
def _add_follow(user_a, user_b):
    try:
        db.session.add(_create_follow(user_a, user_b))
        db.session.commit()
        return 1
    except:
        db.session.rollback()
        return -1


# TODO: use celerity
def _delete_follow(user_a, user_b):
    try:
        item = Followers.query.filter_by(follower_id=user_a, followed_id=user_b).first()
        print(item)
        db.session.delete(item)
        db.session.commit()
        return 1
    except:
        db.session.rollback()
        return -1
