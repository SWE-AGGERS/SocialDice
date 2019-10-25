from monolith.classes.DiceSet import Die, DiceSet
import random as rnd
import unittest
 
class TestDie(unittest.TestCase):
    def test_die_init(self):
        die = Die("./monolith/classes/tests/die0.txt")
        rnd.seed(574891)
        result = die.faces
        print(result)
        self.assertEqual(result, ['bike', 'moonandstars', 'bag', 'bird', 'crying', 'angry'])


class TestDice(unittest.TestCase):

    def test_dice_init(self):
        dice = DiceSet("./monolith/resources/basic_set")
        self.assertEqual(len(dice.dice), 6)

        check1 = ['tulip', 'mouth', 'caravan', 'clock', 'whale', 'drink']
        self.assertEqual(dice.dice[1].faces, check1)

    
 
 
if __name__ == '__main__':
    unittest.main()