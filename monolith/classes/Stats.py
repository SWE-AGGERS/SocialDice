from monolith.database import Story, db, Reaction
from sqlalchemy.sql import func


class Stats():
    likes: int
    dislikes: int

    def __init__(self, user_id):
        q_stories = db.session.query(Story).filter(Story.author == user_id)

        for s in q_stories:
            q_react = db.session.query(func.max())





