from monolith.database import db, Story, Reaction
from sqlalchemy import and_


@event.listen_for(Story, '<??>')
def send_telegram_message():
    # get the story author id
    # get follower's id of the author
    # for each user
    # get the chat id
    # send a message with "user.firstname user.lastname write a new story! Check it out!"
    # close