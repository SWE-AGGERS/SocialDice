from flask import Blueprint, render_template, redirect, request
from flask_login import (current_user, login_user, logout_user,
                         login_required)

from monolith.database import db, User
from monolith.forms import LoginForm
from monolith.forms import UserForm

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    message = ""
    error = False
    if form.validate_on_submit():
        email, password = form.data['email'], form.data['password']
        q = db.session.query(User).filter(User.email == email)
        user = q.first()

        if user is not None and user.authenticate(password):
            login_user(user)
            return redirect('/')
        else:
            message = "User not found"
            error = True

    return render_template('login.html', form=form, error=error, message=message)


@auth.route("/logout")
def logout():
    logout_user()
    return redirect('/')


@auth.route("/signup", methods=['POST', 'GET'])
def signup():
    form = UserForm()
    if request.method == 'POST':
        email = form.data['email']

        q = db.session.query(User).filter(User.email == email)
        check = q.first()
        if check is None:
            user = User()
            user.firstname = form.data['firstname']
            user.lastname = form.data['lastname']
            user.email = form.data['email']
            user.dateofbirth = form.data['dateofbirth']
            user.set_password(form.data['password'])
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect("/")
        else:
            form = UserForm()

            return render_template('signup.html', form=form, error=True, message="The email was used before. Please change the email!" )
    if request.method == 'GET':
        return render_template('signup.html', form=form)
