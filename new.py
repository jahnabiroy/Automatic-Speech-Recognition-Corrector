from itertools import product
import json
def recover_word(misread_word, misread_dict, english_words):
    def generate_words(word, index=0):
        if index == len(word):
            yield ''.join(word)
            return

        if word[index] in misread_dict:
            for char in misread_dict[word[index]]:
                word[index] = char
                yield from generate_words(word, index + 1)
        else:
            yield from generate_words(word, index + 1)

    possible_words = generate_words(list(misread_word))
    return [word for word in possible_words if word in english_words]


misread_dict = {}
with open("data/phoneme_table.json", "r") as file:
    misread_dict = json.load(file)

english_words = set(["SHOY", "TOY", "ROY"])

misread_word = 'SOY'
original_words = recover_word(misread_word, misread_dict, english_words)
print(f"Possible original words for '{misread_word}': {original_words}")
