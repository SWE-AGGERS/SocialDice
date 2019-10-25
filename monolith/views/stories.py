from flask import Blueprint, redirect, render_template, request
from monolith.database import db, Story, Like, Reaction
from monolith.auth import admin_required, current_user
from flask_login import (current_user, login_user, logout_user,
                         login_required)
from monolith.forms import UserForm

stories = Blueprint('stories', __name__)

@stories.route('/stories')
def _stories(message=''):
    allstories = db.session.query(Story)
    return render_template("stories.html", message=message, stories=allstories)


@stories.route('/story/<storyid>/reaction/<reactiontype>', methods=['GET']) # reactionid= 1,2
#@login_required
# TODO add counters for stories
def _reaction(storyid, reactiontype):
    # check if story exist
    q = Story.query.filter_by(id=storyid).first()
    if q is None:
        message = 'Story doent exist!'
        return _stories(message)

    if 'GET' == request.method:
        # q = Reaction.query.filter_by(liker_id=current_user.id, story_id=storyid)
        q = Reaction.query.filter_by(reaction_id=1, story_id=storyid).first()
        if q is None: # no reactions yet
            new_reaction = Reaction()
            # new_reaction.reaction_id = current_user.id
            new_reaction.reaction_id = 1
            new_reaction.story_id = storyid
            new_reaction.type = reactiontype
            db.session.add(new_reaction)
            db.session.commit()
            # TODO CELERY
            # if int(type) == 1: #like
            #     increase_likes()
            # elif int(type) == 2: #dislike
            #     increase_dislikes()

            message = 'Reaction to story created!'
        else:
            print(q.to_string())
            # check if the reaction already present is the same of the newone
            if int(reactiontype) == int(q.type):
                message = 'You already react in this way!'
            else:
                q.type = reactiontype
                db.session.commit()
                message = 'You change your reaction!'
        return _stories(message)

    elif 'DELETE' == request.method:
        q = Reaction.query.filter_by(reaction_id=1, story_id=storyid).first()
        if q is None:  # reaction doen't exist
            message = 'You never reacted!'
        else:
            db.session.delete(q)
            db.session.commit()
            message = 'Reaction removed'
        return _stories(message)
