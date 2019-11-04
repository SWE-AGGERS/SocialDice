from flask import Blueprint, redirect, render_template, request

from monolith.database import db, User, Story
from monolith.forms import UserForm
from sqlalchemy import desc

users = Blueprint('users', __name__)


def reduce_list(users_):
    users = []
    aux = []
    for user, story in users_:
        if user.id not in aux:
            users.append(
                (user, story)
            )
            aux.append(user.id)

    return users


@users.route('/users')
def _users():
    users = db.session.query(User, Story).join(Story).order_by(desc(Story.id))
    users = reduce_list(users.all())
    return render_template("users.html", users=users)
