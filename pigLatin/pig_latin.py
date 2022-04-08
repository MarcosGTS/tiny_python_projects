"""Translate a English text to Pig latin """

def main():
    """
    Receive a text input from user
    print a pig-latin version of the text
    """

    text = input("Text to translate")
    result = []

    for word in text.split():
        result += [translate_to_piglatin(word)]

    print(" ".join(result))

def is_capitalized(word):
    """check if word is captalized"""
    return word[0].isupper() and word[1:].islower()

def translate_to_piglatin(word):
    """Return a traslated word"""

    normalized_copy = word.lower()
    translated = ""

    if normalized_copy[0] in "aeiou":
        translated = normalized_copy + "way"
    else:
        translated = normalized_copy[1:] + normalized_copy[0] + "ay"

    return translated.capitalize() if is_capitalized(word) else translated

if __name__ == "__main__":
    main()
