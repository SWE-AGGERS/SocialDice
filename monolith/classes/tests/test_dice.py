from monolith.classes import DiceSet as d
import unittest
import os
from monolith import constants
 
class TestDie(unittest.TestCase):
 
    def test_file_not_found(self):
        path = os.path.join(constants.BASE_PATH, 'monolith/resources/die7.txt')
        self.assertRaises(FileNotFoundError, d.Die,path)

    def test_empty_file(self):
        path = os.path.join(constants.BASE_PATH, 'monolith/resources/die6.txt')
        self.assertRaises(OSError, d.Die,path)




    def test_die_init(self):
        path = os.path.join(constants.BASE_PATH, 'monolith/resources/die0.txt')
        die = d.Die(path)
        check = ['bike', 'moonandstars', 'bag', 'bird', 'crying', 'angry']
        self.assertEqual(die.faces, check)


 
if __name__ == '__main__':
    unittest.main()
