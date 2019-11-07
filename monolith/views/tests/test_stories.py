from monolith.views import check_stories as cs
from monolith.views.check_stories import SizeDiceSetFacesError
from monolith.views.check_stories import TooSmallStoryError
from monolith.views.check_stories import WrongFormatDiceError
from monolith.views.check_stories import WrongFormatSingleDiceError
from monolith.views.check_stories import WrongFormatStoryError
from monolith.views.check_stories import WrongFormatSingleFaceError, InvalidStory
import os
from monolith.classes import DiceSet as d
import unittest
from monolith import constants
 
class TestStory(unittest.TestCase):
 
    def test_valid_story(self):
        diceSet = d.DiceSet('basic')
        die0 = 'bike moonandstars bag bird crying angry'
        die1 = 'tulip mouth caravan clock whale drink'
        die2 = 'happy coffee plate bus letter paws'
        die3 = 'cat pencil baloon bananas phone icecream'
        die4 = 'ladder car fire bang hat hamburger'
        die5 = 'rain heart glasses poo ball sun'
        storySet = die0 + " " + die1 + " " + die2 + " " + die3 + " " + die4 + " " + die5
        roll = diceSet.throw_dice("6")
        self.assertEqual(cs.check_storyV2(storySet,roll),None)


    def test_invalid_story(self):
        diceSet = d.DiceSet('basic')
        storySet = ""
        for elem in range(0,30):
            string = "a"
            storySet = storySet + string + " "
        roll = diceSet.throw_dice("6")
        with self.assertRaises(InvalidStory):
            cs.check_storyV2(storySet, roll)



    def test_invalid_story_wrong_type_story(self):
        diceSet = d.DiceSet('basic')
        roll = diceSet.throw_dice("1")
        with self.assertRaises(WrongFormatStoryError):
            cs.check_storyV2(122, roll)
        #self.assertRaises(WrongFormatStoryError, cs.check_storyV2,122,roll)


    def test_invalid_story_short_story(self):
        diceSet = d.DiceSet('basic')
        die0 = 'bike moonandstars bag bird crying angry'
        die1 = 'tulip mouth caravan clock whale drink'
        die2 = 'happy coffee plate bus letter paws'
        die3 = 'cat pencil baloon bananas phone icecream'
        die4 = 'ladder car fire bang hat hamburger'
        die5 = 'rain heart glasses poo ball sun'
        storySet = ""
        roll = diceSet.throw_dice("6")
        self.assertRaises(TooSmallStoryError, cs.check_storyV2,storySet,roll)

    def test_invalid_story_wrong_type_diceset(self):
        storySet = "a b c"
        roll = "a"
        self.assertRaises(WrongFormatDiceError, cs.check_storyV2,storySet,roll)












 
 
if __name__ == '__main__':
    unittest.main()