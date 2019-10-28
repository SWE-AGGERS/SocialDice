from flask import Blueprint, redirect, render_template, request
from monolith.database import db, Story, Like, User
from monolith.auth import admin_required, current_user
from flask_login import (current_user, login_user, logout_user,
                         login_required)
from monolith.forms import UserForm

stories = Blueprint('stories', __name__)

@stories.route('/stories')
def _stories():
    allstories = db.session.query(Story, User).join(User)
    print(allstories)
    return render_template("stories.html", stories=allstories, like_it_url="http://127.0.0.1:5000/stories/reaction")


@stories.route('/stories/like/<authorid>/<storyid>')
@login_required
def _like(authorid, storyid):
    q = Like.query.filter_by(liker_id=current_user.id, story_id=storyid)
    if q.first() != None:
        new_like = Like()
        new_like.liker_id = current_user.id
        new_like.story_id = storyid
        new_like.liked_id = authorid
        db.session.add(new_like)
        db.session.commit()
        message = ''
    else:
        message = 'You\'ve already liked this story!'
    return _stories(message)
