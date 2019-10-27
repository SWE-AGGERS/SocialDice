from flask import Blueprint, render_template, jsonify

from monolith.database import db, Story, Like, User
from monolith.auth import current_user


wall = Blueprint('wall', __name__)


def _strava_auth_url(config):
    return '127.0.0.1:5000'


@wall.route('/wall')
def getmywall():
    if current_user is not None and hasattr(current_user, 'id'):
        stories = db.session.query(Story).filter(Story.author_id == current_user.id)
    else:
        stories = None
    return render_template("index.html", stories=stories)


@wall.route('/wall/<user_id>')
def getawall(user_id):
    q = db.session.query(User).filter(User.id == user_id)
    user = q.first()
    if user is None:
        return 404

    q = db.session.query(Story).filter(Story.author_id == user.id)
    user_stories = []
    for s in q:
        s: Story
        story = {}
        user_stories.append({'story_id': s.id, 'text': s.text})

    return jsonify(firstname=user.firstname,
                   lastname=user.lastname,
                   email=user.email,
                   stories=user_stories)
