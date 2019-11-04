# encoding: utf8
import datetime as dt

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.Unicode(128), nullable=False)
    firstname = db.Column(db.Unicode(128))
    lastname = db.Column(db.Unicode(128))
    password = db.Column(db.Unicode(128))
    dateofbirth = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    is_anonymous = False

    def __init__(self, *args, **kw):
        super(User, self).__init__(*args, **kw)
        self._authenticated = False

    def set_password(self, password):
        self.password = generate_password_hash(password)

    @property
    def is_authenticated(self):
        return self._authenticated

    def authenticate(self, password):
        checked = check_password_hash(self.password, password)
        self._authenticated = checked
        return self._authenticated

    def get_id(self):
        return self.id


class Story(db.Model):
    __tablename__ = 'story'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    text = db.Column(db.Text(1000))  # around 200 (English) words
    dicenumber = db.Column(db.Integer)
    # textual representation (labels) of dice faces {dice:[...]}
    roll = db.Column(db.JSON)

    date = db.Column(db.DateTime)
    # will store the number of likes, periodically updated in background
    likes = db.Column(db.Integer)
    # will store the number of likes, periodically updated in background
    dislikes = db.Column(db.Integer)
    # define foreign key
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = relationship('User', foreign_keys='Story.author_id')

    def __init__(self, *args, **kw):
        super(Story, self).__init__(*args, **kw)
        self.date = dt.datetime.now()


class Reaction(db.Model):
    __tablename__ = 'reaction'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    reaction = relationship('User', foreign_keys='Reaction.user_id')

    story_id = db.Column(db.Integer, db.ForeignKey(
        'story.id'), primary_key=True)
    author = relationship('Story', foreign_keys='Reaction.story_id')

    type = db.Column(db.Integer)  # 1: like, 2: dislike

    # True iff it has been counted in Story.likes
    marked = db.Column(db.Boolean, default=False)

# ================================================================================================
# Followers Table
# ================================================================================================


class Followers(db.Model):
    """Followers Table: 
    (A, B) -> User A follow user B 
    (A is the follower, B is the followed)"""
    __tablename__ = 'followers'
    followed_id = db.Column(
        db.Integer, db.ForeignKey('user.id'), primary_key=True)
    followed = relationship('User', foreign_keys='Followers.followed_id')

    follower_id = db.Column(
        db.Integer, db.ForeignKey('user.id'), primary_key=True)
    follower = relationship('User', foreign_keys='Followers.follower_id')

    def to_string(self):
        return 'liker_id: ' + str(self.user_id) + \
               '\nstory_id: ' + str(self.story_id) + \
               '\ntype: ' + str(self.type)
