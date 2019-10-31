from flask import Blueprint, request, redirect, render_template, abort
from flask_login import (current_user, login_required)

from monolith.background import update_reactions
from flask_login import (current_user, login_user, logout_user,
                         login_required)
from monolith.forms import UserForm, StoryForm, SelectDiceSetForm
from monolith.database import db, Story, Reaction

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
        text = request.form.get('text')
        roll = request.form.get('roll')
        dicenumber = len(roll)
        new_story.text = text
        new_story.roll = {'dice':str(roll)}
        new_story.dicenumber = dicenumber
        db.session.add(new_story)
        db.session.commit()
        return redirect('/stories')

    if 'GET' == request.method:
        # Go to the feed
        allstories = db.session.query(Story)
        return render_template("stories.html", form=form, message=message, stories=allstories,
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
    q = db.session.query(Story).filter_by(id=storyid)
    story = q.first()
    if story is not None:
        return render_template("story_detail.html", story=story)
    else:
        abort(404)


@stories.route('/rolldice/<dicenumber>/<dicesetid>', methods=['GET'])
def _roll(dicenumber, dicesetid):
    form = StoryForm()
    #dicenumber = request.args.get("dicenumber")
    #dicesetid = request.args.get("dicesetid")
    
    dice = DiceSet(dicesetid)
    
    return render_template("create_story.html", form=form, roll=dice.throw_dice())

