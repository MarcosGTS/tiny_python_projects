import random, sys

NAMES_FILE = "names.txt"
SURNAMES_FILE = "surnames.txt"

def loadNames(fname):
    names = []

    with open(fname) as file:
        for line in file:
            #remove new line caracter
            #add to name list
            names.append(line[:-1])

    return names

first = loadNames(NAMES_FILE)
last  = loadNames(SURNAMES_FILE)

while True:
    firstName = random.choice(first)
    lastName  = random.choice(last)

    print(f"{firstName} {lastName}")
    
    tryAgain = input("\nTry again? (Press Enter else n) \n\n")

    if tryAgain.lower() == "n":
        break

input("Press Enter to exit.")
