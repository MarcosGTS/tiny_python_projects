"""Translate a English text to Pig latin """

def main():
    print(translate_to_piglatin("apple"))
            
def translate_to_piglatin(word):
    """Return a traslated word"""
    
    first_char = word[0]
    translated = ""

    if first_char.lower() in "aeiou":
        translated = word + "way"
    else:
        translated = word[1:] + word[0] + "ay"

    return translated 

if __name__ == "__main__":
    main()
