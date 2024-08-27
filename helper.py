from itertools import product
import json
from hashing import hash_word

def reverse_phoneme_table(phoneme_table):
    reverse_table = {}
    for original, subs in phoneme_table.items():
        for sub in subs:
            if sub not in reverse_table:
                reverse_table[sub] = []
            reverse_table[sub].append(original)
    return reverse_table

def generate_original_possibilities(asr_word, phoneme_table,all_words):
    reverse_table = reverse_phoneme_table(phoneme_table)
    possible_substitutions = []
    for char in asr_word:
        if char in reverse_table:
            possible_substitutions.append(reverse_table[char] + [char])
        else:
            possible_substitutions.append([char])
    all_combinations = product(*possible_substitutions)
    possible_words = [''.join(combo) for combo in all_combinations]
    result = [asr_word]
    for i in possible_words:
        hash_value = hash_word(i)
        if hash_value not in all_words:
            continue
        lst = all_words[hash_value]
        for j in lst:
            if(i == j[0]):
                result.append(i)
    return result

# Example usage
# with open("data/phoneme_table.json", 'r') as f:
#     phoneme_table = json.load(f)

# with open("words.json",'r') as f:
#     all_words = json.load(f)

# asr_word = "GINGS"
# original_possibilities = generate_original_possibilities(asr_word, phoneme_table,all_words)
# for i in original_possibilities:
#     hash_value = hash_word(i)
#     if hash_value not in all_words:
#         continue
#     lst = all_words[hash_value]
#     for j in lst:
#         if(i == j[0]):
#             print(i)
#
# lst = ["ABC","DEF"]
# sentence = " ".join(lst) + "X"
# print(sentence)
