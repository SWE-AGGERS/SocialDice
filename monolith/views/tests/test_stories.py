from monolith.views import check_stories as cs
from monolith.views.check_stories import TooSmallStoryError
from monolith.views.check_stories import TooLongStoryError
from monolith.views.check_stories import WrongFormatDiceError
from monolith.views.check_stories import WrongFormatSingleDiceError
from monolith.views.check_stories import WrongFormatStoryError
from monolith.classes import DiceSet as d
import unittest
 
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
        roll = diceSet.throw_dice(dicenumber=6)
        self.assertEqual(cs.check_storyV2(storySet,roll),True)


    def test_invalid_story(self):
        diceSet = d.DiceSet('basic')
        storySet = ""
        for elem in range(0,30):
            string = "a"
            storySet = storySet + string + " "
        roll = diceSet.throw_dice(dicenumber=6)
        self.assertEqual(cs.check_storyV2(storySet,roll),False)



    def test_invalid_story_wrong_type_story(self):
        diceSet = d.DiceSet('basic')
        roll = diceSet.throw_dice(dicenumber=6)
        self.assertRaises(WrongFormatStoryError, cs.check_storyV2,1,roll)


    def test_invalid_story_short_story(self):
        diceSet = d.DiceSet('basic')
        storySet = ""
        roll = diceSet.throw_dice(dicenumber=6)
        self.assertRaises(TooSmallStoryError, cs.check_storyV2,storySet,roll)


    def test_invalid_story_long_story(self):
        diceSet = d.DiceSet('basic')
        storySet = ""
        for elem in range(0,1001):
            string = "a"
            storySet = storySet + string + " "
        roll = diceSet.throw_dice(dicenumber=6)
        self.assertRaises(TooLongStoryError, cs.check_storyV2,storySet,roll)



    def test_invalid_story_wrong_type_diceset(self):
        storySet = "a b c"
        roll = 1
        self.assertRaises(WrongFormatDiceError, cs.check_storyV2,storySet,roll)





    def test_invalid_story_wrong_type_dice(self):
        diceSet = d.DiceSet('basic')
        die0 = 'bike moonandstars bag bird crying angry'
        die1 = 'tulip mouth caravan clock whale drink'
        die2 = 'happy coffee plate bus letter paws'
        die3 = 'cat pencil baloon bananas phone icecream'
        die4 = 'ladder car fire bang hat hamburger'
        die5 = 'rain heart glasses poo ball sun'
        storySet = die0 + " " + die1 + " " + die2 + " " + die3 + " " + die4 + " " + die5
        roll = diceSet.throw_dice(dicenumber=6)
        roll.append(1)
        self.assertRaises(WrongFormatSingleDiceError, cs.check_storyV2,storySet,roll)




 
 
if __name__ == '__main__':
    unittest.main()
