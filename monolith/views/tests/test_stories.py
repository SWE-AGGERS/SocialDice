from monolith.views import check_stories as cs
from monolith.views.check_stories import SizeDiceSetFacesError
from monolith.views.check_stories import TooSmallStoryError
from monolith.views.check_stories import WrongFormatDiceError
from monolith.views.check_stories import WrongFormatSingleDiceError
from monolith.views.check_stories import WrongFormatStoryError
from monolith.views.check_stories import WrongFormatSingleFaceError
import os
from monolith.classes import DiceSet as d
import unittest
import constants
 
class TestStory(unittest.TestCase):
 
    def test_valid_story(self):
        diceSet = []
        path = os.path.join(constants.BASE_PATH, 'monolith/resources/dice0.txt')
        diceSet.append(d.Dice(path))
        path = os.path.join(constants.BASE_PATH, 'monolith/resources/dice1.txt')
        diceSet.append(d.Dice(path))
        ds = d.DiceSet(diceSet)
        ds.throw_dice()
        self.assertEqual(cs.check_storyV2("bike moonandstars bag bird crying angry tulip mouth caravan clock whale drink",ds),True)


    def test_invalid_story(self):
        diceSet = []
        path = os.path.join(constants.BASE_PATH, 'monolith/resources/dice0.txt')
        diceSet.append(d.Dice(path))
        path = os.path.join(constants.BASE_PATH, 'monolith/resources/dice1.txt')
        diceSet.append(d.Dice(path))
        ds = d.DiceSet(diceSet)
        ds.throw_dice()
        self.assertEqual(cs.check_storyV2("a a a a a a a a a a a a",ds),False)



    def test_invalid_story_wrong_type_story(self):
        diceSet = []
        path = os.path.join(constants.BASE_PATH, 'monolith/resources/dice0.txt')
        diceSet.append(d.Dice(path))
        path = os.path.join(constants.BASE_PATH, 'monolith/resources/dice1.txt')
        diceSet.append(d.Dice(path))
        ds = d.DiceSet(diceSet)
        ds.throw_dice()
        self.assertRaises(WrongFormatStoryError, cs.check_storyV2,1,ds)


    def test_invalid_story_short_story(self):
        diceSet = []
        path = os.path.join(constants.BASE_PATH, 'monolith/resources/dice0.txt')
        diceSet.append(d.Dice(path))
        path = os.path.join(constants.BASE_PATH, 'monolith/resources/dice1.txt')
        diceSet.append(d.Dice(path))
        ds = d.DiceSet(diceSet)
        ds.throw_dice()
        self.assertRaises(TooSmallStoryError, cs.check_storyV2,"",ds)

    def test_invalid_story_wrong_type_diceset(self):
        diceSet = []
        path = os.path.join(constants.BASE_PATH, 'monolith/resources/dice0.txt')
        diceSet.append(d.Dice(path))
        path = os.path.join(constants.BASE_PATH, 'monolith/resources/dice1.txt')
        diceSet.append(d.Dice(path))
        ds = d.DiceSet(diceSet)
        ds.throw_dice()
        self.assertRaises(WrongFormatDiceError, cs.check_storyV2,"a b c","a")




    def test_invalid_story_equal_number_dice_faces(self):
        diceSet = []
        path = os.path.join(constants.BASE_PATH, 'monolith/resources/dice0.txt')
        diceSet.append(d.Dice(path))
        path = os.path.join(constants.BASE_PATH, 'monolith/resources/dice1.txt')
        diceSet.append(d.Dice(path))
        ds = d.DiceSet(diceSet)
        ds.throw_dice()
        path = os.path.join(constants.BASE_PATH, 'monolith/resources/dice2.txt')
        ds.dice.append(d.Dice(path))
        self.assertRaises(SizeDiceSetFacesError, cs.check_storyV2,"a a a a a a a a a a a a",ds)

    def test_invalid_story_wrong_type_dice(self):
        diceSet = []
        path = os.path.join(constants.BASE_PATH, 'monolith/resources/dice0.txt')
        diceSet.append(d.Dice(path))
        path = os.path.join(constants.BASE_PATH, 'monolith/resources/dice1.txt')
        diceSet.append(d.Dice(path))
        ds = d.DiceSet(diceSet)
        ds.throw_dice()
        ds.dice.append("a")
        ds.pips.append("a")
        self.assertRaises(WrongFormatSingleDiceError, cs.check_storyV2,"a a a a a a a a a a a a",ds)

    def test_invalid_story_wrong_type_faces(self):
        diceSet = []
        path = os.path.join(constants.BASE_PATH, 'monolith/resources/dice0.txt')
        diceSet.append(d.Dice(path))
        ds = d.DiceSet(diceSet)
        ds.throw_dice()
        path = os.path.join(constants.BASE_PATH, 'monolith/resources/dice1.txt')
        diceSet.append(d.Dice(path))
        ds.pips.append(1)
        self.assertRaises(WrongFormatSingleFaceError, cs.check_storyV2,"a a a a a a a a a a a a",ds)



 
 
if __name__ == '__main__':
    unittest.main()