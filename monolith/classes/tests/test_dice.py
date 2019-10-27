from monolith.classes import DiceSet as d
import random as rnd
import unittest
import os
import constants
 
class TestDice(unittest.TestCase):
 
    def test_file_not_found(self):
        path = os.path.join(constants.BASE_PATH, 'monolith/resources/dice7.txt')
        self.assertRaises(FileNotFoundError, d.Dice,path)

    def test_empty_file(self):
        path = os.path.join(constants.BASE_PATH, 'monolith/resources/dice6.txt')
        self.assertRaises(OSError, d.Dice,path)




    def test_dice_init(self):
        path = os.path.join(constants.BASE_PATH, 'monolith/resources/dice0.txt')
        die = d.Dice(path)
        check = ['bike', 'moonandstars', 'bag', 'bird', 'crying', 'angry']
        self.assertEqual(die.faces, check)


 
if __name__ == '__main__':
    unittest.main()