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

    def __init__(self, author: User):
        self.id = author.id
        self.email = author.email
        self.firstname = author.firstname
        self.lastname = author.lastname
        self.stories = []#stories

    def add_story(self, new_story: Story):
        if len(self.stories) >= self.storyLimit:
            self.stories.pop(0)

        self.stories.append(PlainStory(new_story))


import unittest


class TestWall(unittest.TestCase):

    def test_die_init(self):
        some_stories = ['story1', 'story2', 'story3', 'story4', 'story5', 'story6']
        wall = Wall(42, 'abc@defg.com', 'user', 'name', some_stories)

        wall.storyLimit = len(wall.stories_view)
        wall.add_story('an extra story')
        self.assertEqual(len(wall.stories_view), wall.storyLimit)

    def test_die_pip(self):
        rnd.seed(574891)
        die = Die("tests/die0.txt")
        res = die.throw_die()
        self.assertEqual(res, 'bag')


if __name__ == '__main__':
    unittest.main()