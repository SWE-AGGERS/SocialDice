from flask import Blueprint, request, redirect, render_template, abort
from flask_login import (current_user, login_required)

from monolith.background import update_reactions
from monolith.classes.DiceSet import DiceSet
from monolith.database import Reaction
from monolith.database import db, Story
from monolith.forms import StoryForm
from monolith.views.home import index
import sys



stories = Blueprint('stories', __name__)


@stories.route('/stories', methods=['POST', 'GET'])
def _stories(message=''):
    form = StoryForm()
    if 'POST' == request.method:
        # Create a new story
        new_story = Story()
        new_story.author_id = current_user.id
        new_story.likes = 0
        new_story.dislikes = 0
        new_story.roll = {'dice': ['bike', 'tulip', 'happy', 'cat', 'ladder', 'rain']}
        if form.validate_on_submit():
            text = form.data['text']
            new_story.text = text
        db.session.add(new_story)
        db.session.commit()
        return redirect('/stories')

    if 'GET' == request.method:
        # Go to the feed
        allstories = db.session.query(Story)
        return render_template("stories.html", form=form, message=message, stories=allstories, id = current_user.id,
                               like_it_url="http://127.0.0.1:5000/stories/like/")



@stories.route('/story/<storyid>/reaction/<reactiontype>', methods=['GET', 'PUSH'])
@login_required
def _reaction(storyid, reactiontype):
    # check if story exist
    q = Story.query.filter_by(id=storyid).first()
    if q is None:
        message = 'Story doent exist!'
        return _stories(message)
    # TODO need to be changed to PUSH (debug motivation)
    if 'GET' == request.method:
        old_reaction = Reaction.query.filter_by(user_id=current_user.id, story_id=storyid).first()

        if old_reaction is None:
            new_reaction = Reaction()
            new_reaction.user_id = current_user.id
            new_reaction.story_id = storyid
            new_reaction.type = reactiontype
            db.session.add(new_reaction)
            db.session.commit()
            message = 'Reaction to story created!'

        else:
            if int(reactiontype) == int(old_reaction.type):
                message = 'You already react in this way!'
                db.session.delete(old_reaction)
                db.session.commit()
            else:
                old_reaction.type = reactiontype
                db.session.commit()
                message = 'You change your reaction!'
        # Update DB counters
        update_reactions.delay(story_id=storyid)
        return _stories(message)


# todo add dices details on render
@stories.route('/stories/<storyid>', methods=['GET'])
def get_story_detail(storyid):
    # Detail of story id
    if 'GET' == request.method:
        q = db.session.query(Story).filter_by(id=storyid)
        story = q.first()
        if story is not None:
            return render_template("story_detail.html", story=story)
        else:
            abort(404)

@stories.route('/stories/<storyid>/remove/<page>', methods=['GET'])
@login_required
def get_remove_story(storyid,page):
    # Remove story
    q = db.session.query(Story).filter_by(id=storyid)
    story = q.first()
    if story is not None:
        if story.author_id == current_user.id:
            print("story query: "+str(story))
            print("story_id "+str(storyid))
            print("author id "+ str(story.author_id))
            print("current user id " + str(current_user.id))
            reactions = Reaction.query.filter_by(story_id=storyid).all()
            print("Number of reactions of the story: "+str(len(reactions)))
            print("Reactions:")
            print(reactions)
            if reactions is not None:
                for reac in reactions:
                        db.session.delete(reac)
                        db.session.commit()
            reactions = Reaction.query.filter_by(story_id=storyid).all()
            print("Number of reactions after the cancellation of the story: "+str(len(reactions)))
            print(reactions)
            db.session.delete(story)
            db.session.commit()
            #return redirect('/')
            if page == "stories":
                message = "The story has been canceled."
                return _stories(message)
            else:
                return index()
        else:
            # The user can only delete the stories she/he wrote.
            #abort(404)
            #return redirect('/stories')
            message = "The story was written by another user and cannot be deleted."
            return _stories(message)

    else:
        # Story doensn't exist
        abort(404)





@stories.route('/rolldice/<int:dicenumber>/<string:dicesetid>', methods=['GET'])
@login_required
def _roll(dicenumber, dicesetid):
    dice = DiceSet(dicesetid)
    return dice.throw_dice()
