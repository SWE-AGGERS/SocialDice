from flask import Blueprint, redirect, render_template, request
from monolith.database import db, Story, Like
from monolith.auth import admin_required, current_user
from monolith.classes.DiceSet import DiceSet
from flask_login import (current_user, login_user, logout_user,
                         login_required)
from monolith.forms import UserForm, StoryForm, SelectDiceSetForm

stories = Blueprint('stories', __name__)

@stories.route('/stories', methods=['POST', 'GET'])
def _stories(message=''):
    form = SelectDiceSetForm()
    if 'POST' == request.method:
        # Create a new story
        new_story = Story()
        new_story.author_id = current_user.id
        new_story.likes = 0
        new_story.dislikes = 0
        new_story.roll = {'dice':['bike', 'tulip', 'happy', 'cat', 'ladder', 'rain']}
        if form.validate_on_submit():
            text = form.data['text']
            new_story.text = text
        db.session.add(new_story)
        db.session.commit()
        return redirect('/stories')

    if 'GET' == request.method:
        # Go to the feed
        allstories = db.session.query(Story)
        return render_template("stories.html", form=form, message=message, stories=allstories, like_it_url="http://127.0.0.1:5000/stories/like/")


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


@stories.route('/rolldice/<int:dicenumber>/<string:dicesetid>', methods=['GET'])
@login_required
def _roll(dicenumber, dicesetid):
    form = StoryForm()
    dice = DiceSet(dicesetid)
    message = str(dice.throw_dice())
    return render_template("create_story.html", form = form, message= message)