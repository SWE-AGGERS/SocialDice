from flask import Blueprint, render_template, jsonify

from monolith.classes.Wall import Wall
from monolith.database import db, Story, User
from monolith.auth import current_user


wall = Blueprint('wall', __name__)

def User_not_found():
    return jsonify({'code': 404, 'msg': 'User not found'})


def _strava_auth_url(config):
    return '127.0.0.1:5000'


@wall.route('/wall')
def getmywall():
    if current_user is not None and hasattr(current_user, 'id'):
        return getawall(current_user.id)
    else:
        return User_not_found()


@wall.route('/thewall/<user_id>')
def renderWall(user_id):
    q = db.session.query(User).filter(User.id == user_id)
    user = q.first()
    if user is None:
        return User_not_found()

    stories = db.session.query(Story).filter(Story.author_id == user.id)

    render_template("wall.html", user=user, stories=stories)


@wall.route('/wall/<user_id>')
def getawall(user_id):
    # if user_id < 0:
    #     return User_not_found()
    q = db.session.query(User).filter(User.id == user_id)
    user = q.first()
    if user is None:
        return User_not_found()

    q = db.session.query(Story).filter(Story.author_id == user.id)
    thewall: Wall = Wall(user)
    user_stories = []
    for s in q:
        s: Story
        thewall.add_story(s)
        user_stories.append(
            {'story_id': s.id,
             'text': s.text,
             'likes': s.likes,
             'dislikes': s.dislikes
             })
        #user_stories.append(s)

    return jsonify(firstname=user.firstname,
                   lastname=user.lastname,
                   email=user.email,
                   stories=user_stories) # thewall.stories