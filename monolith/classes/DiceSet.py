import glob
import os
import random as rnd
import natsort
import re

# list of all available dice sets
_DICE_SETS = [{'id': 1, 'name': 'basic', 'folder': './monolith/resources/basic_set'}, {'id': 2, 'name':'halloween', 'folder': './monolith/resources/halloween_set'}]


class Die:

    def __init__(self, filename):
        self.faces = []
        self.pip = None
        f = open(filename, "r")
        lines = f.readlines()

        for line in lines:
            self.faces.append(line.replace("\n", ""))
        self.throw_die()
        f.close()

    def throw_die(self):
        if self.faces:  # pythonic for list is not empty
            self.pip = rnd.choice(self.faces)
            return self.pip
        else:
            raise IndexError("throw_die(): empty die error.")


class DiceSet:

    def __init__(self, set_name):
        self.dice = []
        self.pips = []

        dice_folder = ""
        for e in _DICE_SETS:
            if e['name'] == set_name:
                dice_folder = e['folder']

        if dice_folder == "":
            raise NonExistingSetError("Dice set not found")

        folder = glob.glob(os.path.join(dice_folder, '*.txt'))
        sorted(folder)

        for filename in natsort.natsorted(folder, reverse=False):
            die = Die(filename)
            self.dice.append(die)

    def throw_dice(self, dicenumber):
        pattern = re.compile("^[0-9]*$")

        if(pattern.match(dicenumber)):
            dicenumber = int(dicenumber)
            if(dicenumber<=0 or dicenumber>len(self.dice)):
                raise WrongDiceNumberError("Wrong dice number!")
            else:
                for i in range(dicenumber):
                    self.pips.append(self.dice[i].throw_die())
        else:
            raise WrongArgumentTypeError("Dice number needs to be an integer!")

        return self.pips


class NonExistingSetError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class WrongArgumentTypeError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class WrongDiceNumberError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)