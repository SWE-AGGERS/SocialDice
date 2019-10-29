from celery import Celery

from monolith.database import db, Story, Reaction

BACKEND = BROKER = 'redis://localhost:6379'
celery = Celery(__name__, backend=BACKEND, broker=BROKER)

_APP = None


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
        num_likes = db.session.query(Reaction.story_id).filter_by(story_id=story_id, type=1).count()
        num_dislikes = db.session.query(Reaction.story_id).filter_by(story_id=story_id, type=2).count()
        # update likes and dislikes counters
        q.likes = num_likes
        q.dislikes = num_dislikes
        db.session.commit()
