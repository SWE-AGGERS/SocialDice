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
        diceSet.throw_dice(6)
        self.assertEqual(cs.check_storyV2(storySet,diceSet),True)


    def test_invalid_story(self):
        diceSet = d.DiceSet('basic')
        storySet = ""
        for elem in range(0,30):
            string = "a"
            storySet = storySet + string + " "
        diceSet.throw_dice(6)
        self.assertEqual(cs.check_storyV2(storySet,diceSet),False)



    def test_invalid_story_wrong_type_story(self):
        diceSet = d.DiceSet('basic')
        die0 = 'bike moonandstars bag bird crying angry'
        die1 = 'tulip mouth caravan clock whale drink'
        die2 = 'happy coffee plate bus letter paws'
        die3 = 'cat pencil baloon bananas phone icecream'
        die4 = 'ladder car fire bang hat hamburger'
        die5 = 'rain heart glasses poo ball sun'
        storySet = die0 + " " + die1 + " " + die2 + " " + die3 + " " + die4 + " " + die5
        diceSet.throw_dice(6)
        self.assertRaises(WrongFormatStoryError, cs.check_storyV2,1,diceSet)


    def test_invalid_story_short_story(self):
        diceSet = d.DiceSet('basic')
        die0 = 'bike moonandstars bag bird crying angry'
        die1 = 'tulip mouth caravan clock whale drink'
        die2 = 'happy coffee plate bus letter paws'
        die3 = 'cat pencil baloon bananas phone icecream'
        die4 = 'ladder car fire bang hat hamburger'
        die5 = 'rain heart glasses poo ball sun'
        storySet = ""
        diceSet.throw_dice(6)
        self.assertRaises(TooSmallStoryError, cs.check_storyV2,storySet,diceSet)

    def test_invalid_story_wrong_type_diceset(self):
        storySet = "a b c"
        diceSet = "a"
        self.assertRaises(WrongFormatDiceError, cs.check_storyV2,storySet,diceSet)




    def test_invalid_story_equal_number_dice_faces(self):
        diceSet = d.DiceSet('basic')
        die0 = 'bike moonandstars bag bird crying angry'
        die1 = 'tulip mouth caravan clock whale drink'
        die2 = 'happy coffee plate bus letter paws'
        die3 = 'cat pencil baloon bananas phone icecream'
        die4 = 'ladder car fire bang hat hamburger'
        die5 = 'rain heart glasses poo ball sun'
        storySet = die0 + " " + die1 + " " + die2 + " " + die3 + " " + die4 + " " + die5
        diceSet.throw_dice(5)
        path = os.path.join(constants.BASE_PATH, 'monolith/resources/basic_set/die2.txt')
        diceSet.dice.append(d.Die(path))
        storySet = storySet + die2
        self.assertRaises(SizeDiceSetFacesError, cs.check_storyV2,storySet,diceSet)

    def test_invalid_story_wrong_type_dice(self):
        diceSet = d.DiceSet('basic')
        die0 = 'bike moonandstars bag bird crying angry'
        die1 = 'tulip mouth caravan clock whale drink'
        die2 = 'happy coffee plate bus letter paws'
        die3 = 'cat pencil baloon bananas phone icecream'
        die4 = 'ladder car fire bang hat hamburger'
        die5 = 'rain heart glasses poo ball sun'
        storySet = die0 + " " + die1 + " " + die2 + " " + die3 + " " + die4 + " " + die5
        diceSet.throw_dice(6)
        diceSet.dice.append("a")
        diceSet.pips.append("a")
        self.assertRaises(WrongFormatSingleDiceError, cs.check_storyV2,storySet,diceSet)

    def test_invalid_story_wrong_type_faces(self):
        diceSet = d.DiceSet('basic')
        die0 = 'bike moonandstars bag bird crying angry'
        die1 = 'tulip mouth caravan clock whale drink'
        die2 = 'happy coffee plate bus letter paws'
        die3 = 'cat pencil baloon bananas phone icecream'
        die4 = 'ladder car fire bang hat hamburger'
        die5 = 'rain heart glasses poo ball sun'
        storySet = die0 + " " + die1 + " " + die2 + " " + die3 + " " + die4 + " " + die5
        diceSet.throw_dice(6)
        path = os.path.join(constants.BASE_PATH, 'monolith/resources/basic_set/die1.txt')
        diceSet.dice.append(d.Die(path))
        diceSet.pips.append(1)
        storySet = storySet + die1
        self.assertRaises(WrongFormatSingleFaceError, cs.check_storyV2,storySet,diceSet)



 
 
if __name__ == '__main__':
    unittest.main()
