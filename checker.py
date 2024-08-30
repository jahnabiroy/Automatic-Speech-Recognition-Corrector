import json
from hashing import hash_word
sentence = json.load(open('outputs.json'))
all_words = json.load(open('words.json'))
for sen in sentence:
    words = sen.split()
    for w in words:
        key = hash_word(w)
        if key not in all_words:
            print(f"Word '{w}' is misspelled")
            continue
