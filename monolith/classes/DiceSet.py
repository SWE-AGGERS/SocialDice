import random as rnd
import os


class Dice:

    def __init__(self, filename):
        self.faces = []
        self.pip = None
        if not filename.endswith("txt"):
            raise ValueError("The file must be a txt file")
        if os.stat(filename).st_size == 0:
            raise OSError("The file is empty")
        f = open(filename, "r")
        lines = f.readlines()
        for line in lines:
           self.faces.append(line.replace("\n",""))
        f.close()

    def throw_dice(self):
        if self.faces:
            self.pip = rnd.choice(self.faces)
            return self.pip
        else:
            raise IndexError("No words found in the file")

class DiceSet:

    def __init__(self, dice):
        if len(dice) == 0:
            raise ValueError("The number of elements of the dice set must be > 0")
        self.dice = dice
        self.pips = []



    def throw_dice(self):
        for i in range(0,len(self.dice)):
            self.pips.append(self.dice[i].throw_dice())
        print("The resulted faces are:"+str(self.pips))
        return self.pips

