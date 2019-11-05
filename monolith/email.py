from celery import Celery
from celery.schedule import crontab
from monolith.constants import _EMAIL, _PASSWORD
from monolith.database import db, Users
from monolith.views.follow import _get_followers_of
# emails library
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

celery_app = Celery()
celery_app.conf.beat_schedule = {
    # Executes every morning at 7:30 a.m.
    'add-every-morning': {
        'task': 'tasks.send_emails',
        'schedule': crontab(hour=7, minute=30)
    },
}
app.conf.timezone = 'UTC'

@celery_app.task
def send_emails():
	# STARTING MAIL SERVER
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(_EMAIL, _PASSWORD)

	# Get all users
	user_tab = get_users()

	# Send an email with news to all users
	for user in user_tab:
		msg = MIMEMultipart()
		msg['From'] = _EMAIL
		msg['To'] = user_email
		msg['Subject'] = 'SocialDice - News!'
		message = make_message(user)
		msg.attach(MIMEText(message))
		server.sendmail(msg)


def get_users():
	"""Return all the users in the db"""
	return Users.query.all()


def maker_message(user):
	"""Make personalized message for each user"""
	text = "Hello "+user.name
	followed_lists = _get_followers_of(user.id)
	if followed_lists == []:
		return text+",\n\nYou have no news for today, take a look and add new writers on Sweaggers' SocialDice!"
	else:
		text +=",\n\nhere you can find what's new on the wall of Sweaggers' SocialDice!\n\n"

	for followed in followed_list:
		# get all stories of a follower posted in the last 24h
		# count them
		# put a line in the text with "> <followed_user_name> poste <stories_number> new stories!"

	text += "\nSee you on SocialDice,\nSeaggers Team"

	return text