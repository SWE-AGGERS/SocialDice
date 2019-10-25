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
    if form.validate_on_submit():
        email, password = form.data['email'], form.data['password']
        q = db.session.query(User).filter(User.email == email)
        user = q.first()
        print(q.first().id)
        if user is not None and user.authenticate(password):
            login_user(user)
            return redirect('/')
    return render_template('login.html', form=form)


@auth.route("/logout")
def logout():
    logout_user()
    return redirect('/')


@auth.route("signup", methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        data = request.get_json()
        q = db.session.query(User).filter(User.email == data['email'])
        check = q.first()
        if check is None:
            user = User()
            user.firstname = data['firstname']
            user.lastname = data['lastname']
            user.email = data['email']
            user.dateofbirth = data['dateofbirth']
            user.set_password(data['password'])
            db.session.add(user)
            db.session.commit()
        else:
            form = UserForm()
            return render_template('signup.html', form=form, error=True, message="The email was used before. Please change the email!" )
    if request.method == 'GET':
        form = UserForm()
        return render_template('signup.html', form=form)
