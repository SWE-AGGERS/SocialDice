from monolith.classes import DiceSet as ds
import nltk
nltk.download('wordnet')


def check_storyV2(story,diceSet):
    # Tests on parameters
    if not isinstance(story, str):
        raise WrongFormatStoryError("The story must be a string.\n")
    if len(story)>1000:
        raise TooLongStoryError("The story is too long. The length is > 1000 characters\n")
    if not isinstance(diceSet, list):
        raise WrongFormatDiceError("The dice set must be a list.\n")
    res = len(story.split())
    if res < len(diceSet):
        raise TooSmallStoryError(
            "The number of words of the story must greater or equal of the number of resulted faces.\n")
    for elem in diceSet:
        if not isinstance(elem,str):
            raise WrongFormatSingleDiceError("Every dice of the dice set must be a die.\n")

    found = True
    i = 0
    while found and i < len(diceSet):
        arr = []
        synset = nltk.corpus.wordnet.synsets(diceSet[i])
        if len(synset) > 0:
            for j in range(0,len(synset[0].lemmas())):
                arr.append(synset[0].lemmas()[j].name())
        if(diceSet[i] not in arr):
            arr.append(diceSet[i])
        print("Synonyms of word "+diceSet[i]+":")
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

    if not found:
        return InvalidStory



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


class TooLongStoryError(Exception):
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


class InvalidStory(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class WrongFormatSingleFaceError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)