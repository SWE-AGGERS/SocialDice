from flask import Blueprint, render_template
from flask import request
from monolith.database import User, Story
from monolith.auth import current_user
from monolith.database import db, Story
from sqlalchemy import func

search = Blueprint('search', __name__)


@search.route('/search', methods=["GET"])
def index():
    search_text = request.args.get("search_text")
    if search_text:
        users = find_user(text=search_text)
        stories = find_story(text=search_text)
        if users and stories:
            return render_template("search.html", users=users, stories=stories)
        elif users:
            return render_template("search.html", users=users)
        elif stories:
            return render_template("search.html", stories=stories)
        else:
            return render_template("search.html")
    else:
        return render_template("search.html")


def find_user(text):
    parameters = text.split()
    users = []

    if len(parameters) == 2:
        r1 = User.query.filter(func.lower(User.firstname) == func.lower(parameters[0]))
        for user in r1:
            users.append(user)
        r2 = User.query.filter(func.lower(User.lastname) == func.lower(parameters[1]))
        for user in r2:
            users.append(user)

    elif len(parameters) == 1:
        r1 = User.query.filter(func.lower(User.firstname) == func.lower(parameters[0]))
        for user in r1:
            users.append(user)
        r2 = User.query.filter(func.lower(User.lastname) == func.lower(parameters[0]))
        for user in r2:
            users.append(user)

    return users if len(users) > 0 else None


def find_story(text):
    result = Story.query.filter(func.lower(Story.text).contains(func.lower(text)))
    return result if result.count() > 0 else None
