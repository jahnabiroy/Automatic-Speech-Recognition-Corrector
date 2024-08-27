import json
phenome = json.load(open('data/phoneme_table.json'))
vocab = json.load(open('data/vocabulary.json'))

print(len(phenome))
print(len(vocab))
