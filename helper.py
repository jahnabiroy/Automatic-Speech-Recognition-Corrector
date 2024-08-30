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


def local_beam_search(asr_word, phoneme_table, all_words, beam_width, max_iterations):
    reverse_table = reverse_phoneme_table(phoneme_table)
    possible_substitutions = [asr_word]
    for char in asr_word:
        if char in reverse_table:
            possible_substitutions.append(reverse_table[char] + [char])
        else:
            possible_substitutions.append([char])
    all_combinations = product(*possible_substitutions)
    possible_words = ["".join(combo) for combo in all_combinations]
    frequency_list = []  # List to store words with their frequencies
    result = []
    for i in possible_words:
        hash_value = hash_word(i)
        if hash_value not in all_words:
            continue
        lst = all_words[hash_value]
        for j in lst:
            if i == j[0]:
                result.append(i)
                frequency_list.append((i, j[1]))  # Add (word, frequency) to frequency list

    # Sort frequency_list by occurrences in descending order
    frequency_list.sort(key=lambda x: x[1], reverse=True)

    # Extract top k words
    top_k_words = [word for word, freq in frequency_list[:beam_width]]
    return top_k_words
