from monolith.classes.DiceSet import Die
import random as rnd
import unittest
 
class TestDie(unittest.TestCase):
    def test_die_init(self):
        die = Die("./monolith/classes/tests/die0.txt")
        rnd.seed(574891)
        result = die.faces
        print(result)
        self.assertEqual(result, ['bike', 'moonandstars', 'bag', 'bird', 'crying', 'angry'])

    
 
 
if __name__ == '__main__':
    unittest.main()