import pprint

DICT_PATH = "/usr/share/dict/words"

#load words
def load_dictionary (f):
    try:
        with open(f) as in_file:
            loaded_words = in_file.read().strip().split("\n")
            loaded_words = [word.lower() for word in loaded_words]
            return loaded_words
    except IOError as e:
        print("{}\nError opening file {}. Terminating program.\n".format(e, f))

#verify palidromes
def is_palindrom (word):
    if len (word) < 2:
        return True
    elif word[0] == word[-1]:
        return is_palindrom(word[1:-1])
    else:
        return False

#display to user
words = load_dictionary ("/usr/share/dict/words")
result = []

for w in words:
    if is_palindrom(w):
        result += [w]

pprint.pprint(result)
