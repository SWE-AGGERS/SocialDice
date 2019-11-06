from flask import Blueprint, request, redirect, render_template, abort, json
from flask_login import (current_user, login_required)

from monolith.background import update_reactions
from flask import Blueprint, redirect, render_template, request
from monolith.auth import admin_required, current_user
from flask_login import (current_user, login_user, logout_user,
                         login_required)
from monolith.forms import UserForm, StoryForm, SelectDiceSetForm
from monolith.database import db, Story, Reaction, User
from monolith.classes.DiceSet import DiceSet, WrongDiceNumberError, NonExistingSetError

from monolith.views.follow import _is_follower
import re
from monolith.views.home import index
from monolith.views.check_stories import check_storyV2
from monolith.views.check_stories import TooSmallStoryError
from monolith.views.check_stories import TooLongStoryError
from monolith.views.check_stories import WrongFormatDiceError
from monolith.views.check_stories import WrongFormatSingleDiceError
from monolith.views.check_stories import WrongFormatStoryError
import sys


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

        if form.validate_on_submit():
            text = request.form.get('text')
            roll = request.form.get('roll')
            # for the tests
            if re.search('"', roll):
                roll = json.loads(request.form.get('roll'))
        arr = roll.split("'")
        arr_final = []
        i = 0
        for elem in range(0,len(arr)):
            if ((i%2!=0)):
                arr_final.append(arr[i])
            i = i + 1
        dicenumber = len(arr_final)
        try:
            if check_storyV2(text, arr_final):
                new_story.text = text
                new_story.roll = {'dice': roll}
                new_story.dicenumber = dicenumber
                db.session.add(new_story)
                db.session.commit()
                message = "Story created!"
                allstories = db.session.query(Story, User).join(User).all()
                allstories = list(
                    map(lambda x: (
                        x[0],
                        x[1],
                        "hidden" if x[1].id == current_user.id else "",
                        "delete" if _is_follower(current_user.id, x[1].id) else "post",
                    ), allstories)
                )
                return render_template(
                    "stories.html",
                    message=message,
                    form=form,
                    stories=allstories,
                    id=current_user.id,
                    active_button="stories",
                    like_it_url="/stories/reaction",
                    details_url="/stories"
                )
            else:
                message = "Invalid story. Try again!"
                allstories = db.session.query(Story, User).join(User).all()
                allstories = list(
                    map(lambda x: (
                        x[0],
                        x[1],
                        "hidden" if x[1].id == current_user.id else "",
                        "delete" if _is_follower(current_user.id, x[1].id) else "post",
                    ), allstories)
                )
                return render_template(
                    "stories.html",
                    message=message,
                    form=form,
                    stories=allstories,
                    id=current_user.id,
                    active_button="stories",
                    like_it_url="/stories/reaction",
                    details_url="/stories"
                )
        except WrongFormatStoryError:
            print('ERROR 1', file=sys.stderr)
            message = "There was an error. Try again."
            allstories = db.session.query(Story, User).join(User).all()
            allstories = list(
                map(lambda x: (
                    x[0],
                    x[1],
                    "hidden" if x[1].id == current_user.id else "",
                    "delete" if _is_follower(current_user.id, x[1].id) else "post",
                ), allstories)
            )
            return render_template(
                "stories.html",
                message=message,
                form=form,
                stories=allstories,
                id=current_user.id,
                active_button="stories",
                like_it_url="/stories/reaction",
                details_url="/stories"
            )
        except WrongFormatDiceError:
            print('ERROR 2', file=sys.stderr)
            message = "There was an error. Try again."
            allstories = db.session.query(Story, User).join(User).all()
            allstories = list(
                map(lambda x: (
                    x[0],
                    x[1],
                    "hidden" if x[1].id == current_user.id else "",
                    "delete" if _is_follower(current_user.id, x[1].id) else "post",
                ), allstories)
            )
            return render_template(
                "stories.html",
                message=message,
                form=form,
                stories=allstories,
                id=current_user.id,
                active_button="stories",
                like_it_url="/stories/reaction",
                details_url="/stories"
            )
        except TooLongStoryError:
            print('ERROR 3', file=sys.stderr)
            message = "The story is too long. The length is > 1000 characters."
            allstories = db.session.query(Story, User).join(User).all()
            allstories = list(
                map(lambda x: (
                    x[0],
                    x[1],
                    "hidden" if x[1].id == current_user.id else "",
                    "delete" if _is_follower(current_user.id, x[1].id) else "post",
                ), allstories)
            )
            return render_template(
                "stories.html",
                message=message,
                form=form,
                stories=allstories,
                id=current_user.id,
                active_button="stories",
                like_it_url="/stories/reaction",
                details_url="/stories"
            )
        except TooSmallStoryError:
            print('ERROR 4', file=sys.stderr)
            message = "The number of words of the story must greater or equal of the number of resulted faces."
            allstories = db.session.query(Story, User).join(User).all()
            allstories = list(
                map(lambda x: (
                    x[0],
                    x[1],
                    "hidden" if x[1].id == current_user.id else "",
                    "delete" if _is_follower(current_user.id, x[1].id) else "post",
                ), allstories)
            )
            return render_template(
                "stories.html",
                message=message,
                form=form,
                stories=allstories,
                id=current_user.id,
                active_button="stories",
                like_it_url="/stories/reaction",
                details_url="/stories"
            )
        except WrongFormatSingleDiceError:
            print('ERROR 5', file=sys.stderr)
            message = "There was an error. Try again."
            allstories = db.session.query(Story, User).join(User).all()
            allstories = list(
                map(lambda x: (
                    x[0],
                    x[1],
                    "hidden" if x[1].id == current_user.id else "",
                    "delete" if _is_follower(current_user.id, x[1].id) else "post",
                ), allstories)
            )
            return render_template(
                "stories.html",
                message=message,
                form=form,
                stories=allstories,
                id=current_user.id,
                active_button="stories",
                like_it_url="/stories/reaction",
                details_url="/stories"
            )

    elif 'GET' == request.method:
        allstories = db.session.query(Story, User).join(User).all()
        allstories = list(
            map(lambda x: (
                x[0],
                x[1],
                "hidden" if x[1].id == current_user.id else "",
                "delete" if _is_follower(current_user.id, x[1].id) else "post",
            ), allstories)
        )
        return render_template(
            "stories.html",
            message=message,
            form=form,
            stories=allstories,
            id=current_user.id,
            active_button="stories",
            like_it_url="/stories/reaction",
            details_url="/stories"
        )











@stories.route('/stories/reaction/<storyid>/<reactiontype>', methods=['GET', 'PUSH'])
@login_required
def _reaction(storyid, reactiontype):
    # check if story exist
    q = Story.query.filter_by(id=storyid).first()
    if q is None:
        message = 'Story doent exist!'
        return _stories(message)
    # TODO need to be changed to PUSH (debug motivation)
    if 'GET' == request.method:
        old_reaction = Reaction.query.filter_by(
            user_id=current_user.id, story_id=storyid).first()

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
    try:
        dice = DiceSet(dicesetid)
    except NonExistingSetError:
        abort(404)

    try:
        roll = dice.throw_dice(int(dicenumber))
    except WrongDiceNumberError:
        return _stories("Wrong dice number!")

    phrase = ""
    for elem in roll:
        phrase = phrase + elem + " "




    return render_template("create_story.html", form=form, set=dicesetid, roll=roll, phrase = phrase)


@stories.route('/stories/<storyid>/remove/<page>', methods=['POST'])
@login_required
def get_remove_story(storyid,page):
    # Remove story
    q = db.session.query(Story).filter_by(id=storyid)
    story = q.first()
    if story is not None:
        if story.author_id == current_user.id:
            reactions = Reaction.query.filter_by(story_id=storyid).all()
            if reactions is not None:
                for reac in reactions:
                        db.session.delete(reac)
                        db.session.commit()
            reactions = Reaction.query.filter_by(story_id=storyid).all()
            db.session.delete(story)
            db.session.commit()
            #return redirect('/')
            if page == "stories":
                message = "The story has been canceled."
                #return _stories(message)
                form = SelectDiceSetForm()
                allstories = db.session.query(Story, User).join(User).all()
                allstories = list(
                    map(lambda x: (
                        x[0],
                        x[1],
                        "hidden" if x[1].id == current_user.id else "",
                        "delete" if _is_follower(current_user.id, x[1].id) else "post",
                    ), allstories)
                )
                return render_template(
                    "stories.html",
                    message=message,
                    form=form,
                    stories=allstories,
                    id=current_user.id,
                    active_button="stories",
                    like_it_url="/stories/reaction",
                    details_url="/stories"
                )
            else:
                return index()
        else:
            # The user can only delete the stories she/he wrote.
            #abort(404)
            #return redirect('/stories')
            message = "The story was written by another user and cannot be deleted."
            #return _stories(message)
            form = SelectDiceSetForm()
            allstories = db.session.query(Story, User).join(User).all()
            allstories = list(
                map(lambda x: (
                    x[0],
                    x[1],
                    "hidden" if x[1].id == current_user.id else "",
                    "delete" if _is_follower(current_user.id, x[1].id) else "post",
                ), allstories)
            )
            return render_template(
                "stories.html",
                message=message,
                form=form,
                stories=allstories,
                id=current_user.id,
                active_button="stories",
                like_it_url="/stories/reaction",
                details_url="/stories"
            )

    else:
        # Story doensn't exist
        abort(404)
