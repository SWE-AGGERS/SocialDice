from monolith.classes import DiceSet as d
import unittest
import os
from monolith import constants





class TestDiceSet(unittest.TestCase):

    def test_number_of_dice_set(self):

        diceSet = []
        path = os.path.join(constants.BASE_PATH, 'resources/dice0.txt')
        diceSet.append(d.Dice(path))
        path = os.path.join(constants.BASE_PATH, 'resources/dice1.txt')
        diceSet.append(d.Dice(path))
        ds = d.DiceSet(diceSet)
        self.assertEqual(len(ds.dice),2)


    def test_number_of_resulting_faces(self):
        diceSet = []
        path = os.path.join(constants.BASE_PATH, 'resources/dice0.txt')
        diceSet.append(d.Dice(path))
        path = os.path.join(constants.BASE_PATH, 'resources/dice1.txt')
        diceSet.append(d.Dice(path))
        ds = d.DiceSet(diceSet)
        self.assertEqual(len(ds.pips),0)


    def test_number_of_resulting_faces_1(self):
        diceSet = []
        path = os.path.join(constants.BASE_PATH, 'resources/dice0.txt')
        diceSet.append(d.Dice(path))
        path = os.path.join(constants.BASE_PATH, 'resources/dice1.txt')
        diceSet.append(d.Dice(path))
        ds = d.DiceSet(diceSet)
        self.assertEqual(len(ds.throw_dice()),2)

    def test_number_of_resulting_faces_equal_number_of_dices(self):
        diceSet = []
        path = os.path.join(constants.BASE_PATH, 'resources/dice0.txt')
        diceSet.append(d.Dice(path))
        path = os.path.join(constants.BASE_PATH, 'resources/dice1.txt')
        diceSet.append(d.Dice(path))
        ds = d.DiceSet(diceSet)
        ds.throw_dice()
        res = (len(ds.pips) == len(ds.dice))
        self.assertEqual(res,True)

    def test_empty_dice_set(self):
        diceSet = []
        self.assertRaises(ValueError, d.DiceSet,diceSet)



if __name__ == '__main__':
    unittest.main()