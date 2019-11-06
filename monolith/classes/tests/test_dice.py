import random as rnd
import unittest

from monolith.classes.DiceSet import Die, DiceSet, WrongArgumentTypeError, WrongDiceNumberError, NonExistingSetError


class TestDie(unittest.TestCase):
    def test_die_init(self):
        die = Die("./monolith/resources/basic_set/die0.txt")
        rnd.seed(574891)
        result = die.faces
        print(result)
        self.assertEqual(result, ['bike', 'moonandstars', 'bag', 'bird', 'crying', 'angry'])


class TestDice(unittest.TestCase):

    def test_dice_init(self):
        # correct init
        dice = DiceSet('basic')
        self.assertEqual(len(dice.dice), 6)

        check1 = ['tulip', 'mouth', 'caravan', 'clock', 'whale', 'drink']
        self.assertEqual(dice.dice[1].faces, check1)

        # non existing dice set
        with self.assertRaises(NonExistingSetError):
            DiceSet('pippo')

    def test_dice_pipes(self):
        dice = DiceSet('basic')
        die0 = ['bike', 'moonandstars', 'bag', 'bird', 'crying', 'angry']
        die1 = ['tulip', 'mouth', 'caravan', 'clock', 'whale', 'drink']
        die2 = ['happy', 'coffee', 'plate', 'bus', 'letter', 'paws']
        die3 = ['cat', 'pencil', 'baloon', 'bananas', 'phone', 'icecream']
        #die4 = ['ladder', 'car', 'fire', 'bang', 'hat', 'hamburger']
        #die5 = ['rain', 'heart', 'glasses', 'poo', 'ball', 'sun']
        result = dice.throw_dice("4")
        #print(result)
        self.assertEqual(len(result), 4)
        self.assertIn(result[0], die0)
        self.assertIn(result[1], die1)
        self.assertIn(result[2], die2)
        self.assertIn(result[3], die3)
        #self.assertIn(result[4], die4)
        #self.assertIn(result[5], die5)

        # wrong argument type
        with self.assertRaises(WrongArgumentTypeError):
            dice.throw_dice("pippo")

        # wrong dice number
        with self.assertRaises(WrongDiceNumberError):
            dice.throw_dice("10")


if __name__ == '__main__':
    unittest.main()
