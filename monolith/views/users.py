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


@users.route('/create_user', methods=['GET', 'POST'])
def create_user():
    form = UserForm()
    if request.method == 'POST':

        if form.validate_on_submit():
            new_user = User()
            form.populate_obj(new_user)
            # pw should be hashed with some salt
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()
            return redirect('/users')

    return render_template('create_user.html', form=form)
