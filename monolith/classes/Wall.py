class Wall:
    storyLimit: int = 50

    def __init__(self, user_id: int, email: str, firstname: str, lastname:str, stories):
        self.id = user_id
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.stories_view = stories

    def add_story(self, new_story):
        if len(self.stories_view) >= self.storyLimit:
            self.stories_view.pop(0)

        self.stories_view.append(new_story)


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