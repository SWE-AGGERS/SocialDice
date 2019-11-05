from monolith.database import Story, db, Reaction
from sqlalchemy.sql import func


class Stats:
    numStories: int
    likes: int
    dislikes: int
    numDice: int

    avgLike: float
    avgDislike: float
    avgDice: float

    ratio_likeDislike: float
    love_level: int

    def __init__(self, user_id):
        self.numStories = db.session.query(Story).filter(Story.author_id == user_id).count()

        # q_likes = db.session.query(Story.likes).filter(Story.author_id == user_id)
        q_likes = db.session.query(func.sum(Story.likes)).filter(Story.author_id == user_id)
        self.likes = q_likes.first()[0]

        q_dislikes = db.session.query(func.sum(Story.dislikes)).filter(Story.author_id == user_id)
        self.dislikes = q_dislikes.first()[0]

        q_numdice = db.session.query(func.sum(Story.dicenumber)).filter(Story.author_id == user_id)
        self.numDice = q_numdice.first()[0]

        self.avgLike = self.likes/self.numStories
        self.avgDislike = self.dislikes / self.numStories
        self.avgDice = self.numDice / self.numStories

        self.ratio_likeDislike = self.likes / self.dislikes

        self.love_level = self.likes - self.dislikes
