from flask import Blueprint, redirect, render_template, request
from monolith.database import db, User
from monolith.auth import admin_required
from monolith.forms import UserForm
from flask_login import login_required

users = Blueprint('users', __name__)

@users.route('/users')
@login_required
def _users():
    users = db.session.query(User)
    return render_template("users.html", users=users,active_button="users")


@users.route('/create_user', methods=['GET', 'POST'])
def create_user():
    form = UserForm()
    if request.method == 'POST':

        if form.validate_on_submit():
            new_user = User()
            form.populate_obj(new_user)
            new_user.set_password(form.password.data) #pw should be hashed with some salt
            db.session.add(new_user)
            db.session.commit()
            return redirect('/users')

    return render_template('create_user.html', form=form)
