from monolith.classes import DiceSet as ds
import nltk
nltk.download('wordnet')



def check_story(story,diceSet):
    # Tests on parameters
    if not isinstance(story, str):
        raise WrongFormatStoryError("The story must be a string.\n")
    res = len(story.split())
    if not isinstance(diceSet,ds.DiceSet):
        raise WrongFormatDiceError("The dice set must be a DiceSet object.\n")
    if res < len(diceSet.pips):
        raise TooSmallStoryError(
            "The number of words of the story must greater or equal of the number of resulted faces.\n")
    if len(diceSet.pips) != len(diceSet.dice):
        raise SizeDiceSetFacesError("The number of resulting faces must be equal to the number of dice.\n")
    for elem in diceSet.dice:
        if not isinstance(elem,ds.Dice):
            raise WrongFormatSingleDiceError("Every dice of the dice set must be a Dice.\n")
    for elem in diceSet.pips:
        if not isinstance(elem,str):
            raise WrongFormatSingleFaceError("Every resulting face of the dice set must be a string.\n")



    found = True
    i = 0
    while found and i<len(diceSet.pips):
        if diceSet.pips[i] not in story:
            found = False
        else:
            i = i+1
    return found



def check_storyV2(story,diceSet):
    # Tests on parameters
    if not isinstance(story, str):
        raise WrongFormatStoryError("The story must be a string.\n")
    res = len(story.split())
    if not isinstance(diceSet,ds.DiceSet):
        raise WrongFormatDiceError("The dice set must be a DiceSet object.\n")
    if res < len(diceSet.pips):
        raise TooSmallStoryError(
            "The number of words of the story must greater or equal of the number of resulted faces.\n")
    if len(diceSet.pips) != len(diceSet.dice):
        raise SizeDiceSetFacesError("The number of resulting faces must be equal to the number of dice.\n")
    for elem in diceSet.dice:
        if not isinstance(elem,ds.Dice):
            raise WrongFormatSingleDiceError("Every dice of the dice set must be a Dice.\n")
    for elem in diceSet.pips:
        if not isinstance(elem,str):
            raise WrongFormatSingleFaceError("Every resulting face of the dice set must be a string.\n")



    found = True
    i = 0
    while found and i<len(diceSet.pips):
        arr = []
        synset = nltk.corpus.wordnet.synsets(diceSet.pips[i])
        if len(synset) > 0:
            for j in range(0,len(synset[0].lemmas())):
                arr.append(synset[0].lemmas()[j].name())
        if(diceSet.pips[i] not in arr):
            arr.append(diceSet.pips[i])
        print("Synonyms of word "+diceSet.pips[i]+":")
        print(arr)
        foundWord = False
        k = 0
        while not foundWord and k<len(arr):
            if arr[k] in story:
                foundWord = True
            else:
             k = k+1
        if not foundWord:
            found = False
        else:
            i = i+1
    return found


class WrongFormatStoryError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class TooSmallStoryError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class WrongFormatDiceError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)





class SizeDiceSetFacesError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)



class WrongFormatSingleDiceError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class WrongFormatSingleFaceError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)