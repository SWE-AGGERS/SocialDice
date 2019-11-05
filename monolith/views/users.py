from flask import Blueprint, redirect, render_template, request

from monolith.database import db, User, Story
from monolith.forms import UserForm
from flask_login import current_user
from sqlalchemy import desc
from monolith.views.follow import _is_follower

users = Blueprint('users', __name__)


def reduce_list(users_):
    users = []
    aux = []
    for user, story in users_:
        if user.id not in aux:
            users.append(
                (story, user)
            )
            aux.append(user.id)

    return users


@users.route('/users')
def _users():
    users = db.session.query(User, Story).join(Story).order_by(desc(Story.id))
    users = reduce_list(users.all())
    users = list(
        map(lambda x: (
            x[0],
            x[1],
            "hidden" if x[1].id == current_user.id else "",
            "unfollow" if _is_follower(
                current_user.id, x[1].id) else "follow",
        ), users)
    )
    return render_template(
        "users.html",
        users=users,
        like_it_url="/stories/reaction"
    )
