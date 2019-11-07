
from monolith.database import db, Story, Followers
from sqlalchemy import and_, desc
import random
from datetime import datetime, timedelta

def get_limit_stories(user_id, min_size=1, max_size_followed=100, 
	max_size_random=20, shuffle=True, day_limit=7, total_max=False):
	# Get all stories in the last X hours 
	# and return them as a list of db object

	# If the total number is less than min, return all
	if Story.query.count() < min_size:
		return Story.query.all()

	counter = 1
	followeds = Followers.query.filter_by(follower_id=user_id).subquery('followeds')
	since = datetime.now() - timedelta(hours=24*day_limit)
	followed_stories = []
	random_stories = []

	if max_size_followed > 0:
		followed_stories = Story.query.filter(and_(
			Story.author_id == followeds.c.followed_id,
			Story.date >= since
			)).order_by(desc(Story.date)).limit(max_size_followed).all()

	if max_size_random > 0:
		if total_max:
			msr = max_size_random + max_size_followed - len(followed_stories)
		else:
			msr = max_size_random
			
		random_stories = Story.query.filter(and_(
			Story.author_id != followeds.c.followed_id,
			)).order_by(desc(Story.date)).limit(msr).all()

	allstories = followed_stories + random_stories

	if shuffle:
		random.shuffle(allstories)
	return allstories
