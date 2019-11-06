from flask import Response

from monolith.database import Story, User


class PlainStory(dict):
    story_id: int
    text: str
    likes: int
    dislikes: int

    def __init__(self, story: Story):
        super().__init__()
        self.story_id = story.id
        self.text = story.text
        self.likes = story.likes
        self.dislikes = story.dislikes


class Wall:
    storyLimit: int = 50
    id: int
    email: str
    firstname: str
    lastname: str
    stories = []

    def __init__(self, author: User = None):
        if author is not None:
            self.id = author.id
            self.email = author.email
            self.firstname = author.firstname
            self.lastname = author.lastname
            self.stories = []#stories

    def add_story(self, new_story: Story):
        if len(self.stories) >= self.storyLimit:
            self.stories.pop(0)

        self.stories.append(PlainStory(new_story))

    def acquire_from_json(self, resp: Response):
        _json = resp.get_json()
        self.id = _json['id']
        self.email = _json['email']
        self.firstname = _json['firstname']
        self.lastname = _json['lastname']
        _stories = _json['stories']
        for st in _stories:
            self.stories.append(st)