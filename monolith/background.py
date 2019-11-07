from celery import Celery

from monolith.database import db, Story, Reaction
from sqlalchemy import and_

# EMAIL IMPORTS
from celery.schedules import crontab
from monolith.constants import _EMAIL, _PASSWORD
from monolith.database import User, Followers
# emails library
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta

BACKEND = BROKER = 'redis://localhost:6379'
celery = Celery(__name__, backend=BACKEND, broker=BROKER)

_APP = None

celery.conf.beat_schedule = {
    # Executes every morning at 7:30 a.m.
    'add-every-morning': {
        'task': 'tasks.send_emails',
        'schedule': crontab(hour=7, minute=30)
    },
}
celery.conf.timezone = 'UTC'


@celery.task
def update_reactions(story_id):
    global _APP
    if _APP is None:
        from monolith.app import create_app
        app = create_app()
        # db.init_app(app)
    else:
        app = _APP
    with app.app_context():
        q = Story.query.filter_by(id=story_id).first()
        # count the likes, dislikes
        # use the first column for efficiency
        # [https://stackoverflow.com/questions/14754994/why-is-sqlalchemy-count-much-slower-than-the-raw-query]
        num_likes = db.session.query(Reaction.story_id).filter_by(
            story_id=story_id, type=1).count()
        num_dislikes = db.session.query(Reaction.story_id).filter_by(
            story_id=story_id, type=2).count()
        # update likes and dislikes counters
        q.likes = num_likes
        q.dislikes = num_dislikes
        db.session.commit()


# PERIODIC DIGEST
@celery.task
def send_emails():
    # STARTING MAIL SERVER
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    try:
        server.login(_EMAIL, _PASSWORD)
    except:
        print("Server login error!")

    # Get all users
    user_tab = get_users()

    result = True
    # Send an email with news to all users
    for user in user_tab:
        msg = MIMEMultipart()
        msg['From'] = _EMAIL
        msg['To'] = user.email
        msg['Subject'] = 'SocialDice - News!'
        message = maker_message(user)
        msg.attach(MIMEText(message))
        try:
            server.sendmail(
                from_addr=_EMAIL,
                to_addrs=user.email,
                msg=msg.as_string()
            )
        except:
            result = False
            continue
    server.quit()
    return result


def maker_message(user):
    """Make personalized message for each user"""
    text = "Hello "+user.firstname
    followed_list = get_followed_list(user.id)
    if followed_list == []:
        return text+",\n\nYou have no news for today, take a look and add new writers on Sweaggers' SocialDice!"
    else:
        text += ",\n\nhere you can find what's new on the wall of Sweaggers' SocialDice!\n"

    for followed in followed_list:
        # get all stories of a follower posted in the last 24h
        # count them)
        stories_number = len(get_all_stories_by_writer(followed))
        f = get_user(followed)
        # put a line in the text with "<followed_user_name> posts <stories_number> new stories!"
        if stories_number > 0:
            text += "\n - "+f.firstname+" "+f.lastname + \
                " posts "+str(stories_number)+" new stories."

    text += "\n\nSee you on SocialDice,\nSweaggers Team"

    return text


def get_all_stories_by_writer(userid):
    since = datetime.now() - timedelta(hours=24)
    try:
        res = Story.query.filter(
            and_(
                Story.author_id == userid,
                Story.date >= since
            )
        ).all()
        return res
    except:
        return []


def get_followed_list(userid):
    return [f.followed.get_id() for f in get_followers_of(userid)]


def get_user(userid):
    return User.query.filter_by(id=userid).first()


def get_users():
    """Return all the users in the db"""
    return User.query.all()

# Get the list of followers of the user_id


def get_followers_of(user_id):
    L = Followers.query.filter_by(follower_id=user_id).all()
    return L
