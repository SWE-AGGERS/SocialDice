from flask import Blueprint, render_template, jsonify
from flask_login import login_required

from monolith.classes.Stats import Stats
from monolith.classes.Wall import Wall
from monolith.database import db, Story, User
from monolith.auth import current_user
from monolith.forms import SelectDiceSetForm
from monolith.views.follow import _is_follower
from monolith.views.stories import reacted

wall = Blueprint('wall', __name__)

def User_not_found():
    return render_template("user_not_found.html")


def _strava_auth_url(config):
    return '127.0.0.1:5000'


# @wall.route('/wall/user_email', methods=['GET'])
# @login_required
# def get_wall_email(user_email):
#     if current_user is not None and hasattr(current_user, 'id'):
#         q = db.session.query(User).filter(User.email == user_email)
#         user = q.first()
#         if user is None:
#             return User_not_found()
#         return render_wall(user.id)


@wall.route('/wall', methods=['GET'])
@login_required
def getmywall():
    if current_user is not None and hasattr(current_user, 'id'):
        return render_wall(current_user.id)


@wall.route('/wall/<user_id>', methods=['GET'])
@login_required
def render_wall(user_id):
    q = db.session.query(User).filter(User.id == user_id)
    user = q.first()
    if user is None:
        return User_not_found()

    stats = Stats(user_id)

    form = SelectDiceSetForm()

    stories = db.session.query(Story, User).join(User).filter(Story.author_id == user.id).all()
    stories = list(
        map(lambda x: (
            x[0],
            x[1],
            "hidden" if x[1].id == current_user.id else "",
            "unfollow" if _is_follower(
                current_user.id, x[1].id) else "follow",
            reacted(current_user.id, x[0].id)
        ), stories)
    )

    rend = render_template(
        "wall.html",
        message='',
        form=form,
        stories=stories,
        active_button="stories",
        like_it_url="/stories/reaction",
        details_url="/stories",
        error=False,
        info_bar=False,
        res_msg=str(''),
        user=user,
        stats=stats
    )

    return rend


@wall.route('/thewall/<user_id>', methods=['GET'])
@login_required
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
                   id=user.id,
                   email=user.email,
                   stories=user_stories) # thewall.stories
