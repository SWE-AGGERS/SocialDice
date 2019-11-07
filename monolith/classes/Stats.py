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
        if not self.numStories:
            self.numStories = 0

        # q_likes = db.session.query(Story.likes).filter(Story.author_id == user_id)
        q_likes = db.session.query(func.sum(Story.likes)).filter(Story.author_id == user_id)
        self.likes = q_likes.first()[0]
        if not self.likes:
            self.likes = 0

        q_dislikes = db.session.query(func.sum(Story.dislikes)).filter(Story.author_id == user_id)
        self.dislikes = q_dislikes.first()[0]
        if not self.dislikes:
            self.dislikes = 0

        q_numdice = db.session.query(func.sum(Story.dicenumber)).filter(Story.author_id == user_id)
        self.numDice = q_numdice.first()[0]
        if not self.numDice:
            self.numDice = 0

        if self.numStories != 0:
            self.avgLike = round(self.likes/self.numStories, 2)
            self.avgDislike = round(self.dislikes / self.numStories, 2)
            self.avgDice = round(self.numDice / self.numStories,2)
        else:
            self.avgLike = 0
            self.avgDislike = 0
            self.avgDice = 0

        if self.dislikes != 0:
            self.ratio_likeDislike = round(self.likes / self.dislikes,2)
        else:
            self.ratio_likeDislike = 0

        self.love_level = self.likes - self.dislikes
