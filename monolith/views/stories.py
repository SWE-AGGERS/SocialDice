from flask import Blueprint, request, redirect, render_template, abort, json, jsonify
from flask_login import (current_user, login_required)
from sqlalchemy import func

from monolith.background import update_reactions
from flask import Blueprint, redirect, render_template, request
from monolith.auth import admin_required, current_user
from flask_login import (current_user, login_user, logout_user,
                         login_required)
from monolith.forms import UserForm, StoryForm, SelectDiceSetForm, StoryFilter
from monolith.database import db, Story, Reaction, User
from monolith.classes.DiceSet import DiceSet, WrongDiceNumberError, NonExistingSetError, WrongArgumentTypeError

from monolith.views.follow import _is_follower
import re

stories = Blueprint('stories', __name__)


@stories.route('/stories', methods=['POST', 'GET'])
def _stories(message='', error=False, res_msg='', info_bar=False):
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

        if(type(roll) is str):
            roll = roll.replace("[", "")
            roll = roll.replace("]", "")
            roll = roll.replace("'", "")
            roll = roll.replace(" ", "")
            aux = roll.split(",")
            roll = aux
            #print(roll)

        dicenumber = len(roll)

        new_story.text = text
        new_story.roll = {'dice': roll}
        new_story.dicenumber = dicenumber
        db.session.add(new_story)
        db.session.commit()
        return redirect('/stories')
    elif 'GET' == request.method:
        allstories = db.session.query(Story, User).join(User).all()
        allstories = list(
            map(lambda x: (
                x[0],
                x[1],
                "hidden" if x[1].id == current_user.id else "",
                "unfollow" if _is_follower(
                    current_user.id, x[1].id) else "follow",
                reacted(current_user.id, x[0].id)
            ), allstories)
        )
        for x in allstories:
            print(x)

        return render_template(
            "stories.html",
            message=message,
            form=form,
            stories=allstories,
            active_button="stories",
            like_it_url="/stories/reaction",
            details_url="/stories",
            error=error,
            info_bar=info_bar,
            res_msg=str(res_msg)
        )


@stories.route('/stories/reaction/<storyid>/<reactiontype>', methods=['GET', 'POST'])
@login_required
def _reaction(storyid, reactiontype):
    try:
        message = add_reaction(reacterid=current_user.id,
                               storyid=storyid, reactiontype=reactiontype)
        # return _stories(error=False, res_msg=message, info_bar=True)
        return jsonify({'reply': message, 'reaction': reactiontype, 'story_id': storyid})
    except StoryNonExistsError as err_msg:
        return _stories(error=True, res_msg=err_msg, info_bar=True)


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
        roll = dice.throw_dice(dicenumber)
    except WrongDiceNumberError:
        return _stories("<div class=\"alert alert-danger alert-dismissible fade show\">" +
                        "<button type=\"button\" class=\"close\" data-dismiss=\"alert\">&times;</button>" +
                        "<strong>Error!</strong> Wrong dice number!</div>")
    except WrongArgumentTypeError:
        return _stories("<div class=\"alert alert-danger alert-dismissible fade show\">" +
                        "<button type=\"button\" class=\"close\" data-dismiss=\"alert\">&times;</button>" +
                        "<strong>Error!</strong> Argument Dice number needs to be an integer!</div>")
    return render_template("create_story.html", form=form, set=dicesetid, roll=roll)


@stories.route('/stories/random', methods=['GET'])
def random_story():
    q = db.session.query(Story).order_by(func.random()).limit(
        1)
    random_story_from_db = q.first()
    return redirect('/stories/'+str(random_story_from_db.id))
#    return render_template("story_detail.html", story=random_story_from_db)


@stories.route('/stories/filter', methods=['GET', 'POST'])
@login_required
def filter_stories():
    if request.method == 'GET':
        form = StoryFilter()
        return render_template('filter_stories.html', form=form)
    if request.method == 'POST':
        form = StoryFilter()
        if form.validate_on_submit():
            init_date = form.init_date.data
            end_date = form.end_date.data
            f_stories = db.session.query(Story, User)\
                .filter(Story.date >= init_date)\
                .filter(Story.date <= end_date)\
                .join(User)\
                .all()
            if f_stories is not None:
                f_stories = list(
                    map(lambda x: (
                        x[0],
                        x[1],
                        "hidden" if x[1].id == current_user.id else "",
                        "unfollow" if _is_follower(
                            current_user.id, x[1].id) else "follow",
                        reacted(current_user.id, x[0].id)
                    ), f_stories))
                return render_template('filter_stories.html',
                                       form=form,
                                       stories=f_stories,
                                       active_button="/stories",
                                       like_it_url="/stories/reaction",
                                       details_url="/stories",
                                       error=False,
                                       info_bar=False
                                       )
        else:
            return render_template('filter_stories.html',
                                   form=form,
                                   info_bar=True,
                                   error=True,
                                   res_msg='Cant travel back in time! Doublecheck dates')


def add_reaction(reacterid, storyid, reactiontype):
    # check if story exist
    q = Story.query.filter_by(id=storyid).first()
    if q is None:
        raise StoryNonExistsError('Story not exists!')

    old_reaction = Reaction.query.filter_by(
        user_id=reacterid, story_id=storyid).first()

    if old_reaction is None:
        new_reaction = Reaction()
        new_reaction.user_id = reacterid
        new_reaction.story_id = storyid
        new_reaction.type = reactiontype
        db.session.add(new_reaction)
        db.session.commit()
        message = 'Reaction created!'

    else:
        if int(reactiontype) == int(old_reaction.type):
            message = 'Reaction removed!'
            db.session.delete(old_reaction)
            db.session.commit()
        else:
            old_reaction.type = reactiontype
            db.session.commit()
            message = 'Reaction changed!'
        # # Update DB counters
    res = update_reactions.delay(story_id=storyid)
    return message


class StoryNonExistsError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def reacted(user_id, story_id):
    q = db.session.query(Reaction).filter_by(
        story_id=story_id, user_id=user_id).all()
    
    if len(q) > 0:
        return q[0].type
    return 0
