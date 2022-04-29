import random

FILE = "dicionario.txt"
WORD_LEN = 5
words = []

def prYellow(str): print("\033[93m {}\033[00m" .format(str), end="")
def prGreen(str): print("\033[92m {}\033[00m" .format(str), end="")
def prDefault(str): print(" {}".format(str), end="")

with open(FILE) as file: 
    for word in file:
        word = word.rstrip()

        if len(word) == WORD_LEN:
            words.append(word)

class CharInfo:
    def __init__ (self, letter):
        self.value = letter 
        self.printFunc = print

    def print (self):
        self.printFunc(self.value)
    
    def set_printFunc(self, printFunc):
        self.printFunc = printFunc

def create_char (word, char, pos):
    char_obj = CharInfo(char)
    
    char_obj.set_printFunc(prDefault)

    if (char in word): char_obj.set_printFunc(prYellow)
    if (word[pos] == char): char_obj.set_printFunc(prGreen)
    
    return char_obj

def compare (word, guess):
    word_obj = []

    for i in range(len(guess)):
        word_obj.append(create_char(word, guess[i], i))

    return word_obj

def render_word(word):
    for char_obj in word:
        char_obj.print()
    print()


render_word(compare("merma", "teste"))