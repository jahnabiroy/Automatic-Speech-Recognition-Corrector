# from itertools import product
# import json
# from hashing import hash_word


# def reverse_phoneme_table(phoneme_table):
#     reverse_table = {}
#     for original, subs in phoneme_table.items():
#         for sub in subs:
#             if sub not in reverse_table:
#                 reverse_table[sub] = []
#             reverse_table[sub].append(original)
#     return reverse_table


# def generate_original_possibilities(asr_word, phoneme_table, all_words):
#     reverse_table = reverse_phoneme_table(phoneme_table)
#     possible_substitutions = []
#     for char in asr_word:
#         if char in reverse_table:
#             possible_substitutions.append(reverse_table[char] + [char])
#         else:
#             possible_substitutions.append([char])
#     all_combinations = product(*possible_substitutions)
#     possible_words = ["".join(combo) for combo in all_combinations]
#     result = [asr_word]
#     for i in possible_words:
#         hash_value = hash_word(i)
#         if hash_value not in all_words:
#             continue
#         lst = all_words[hash_value]
#         for j in lst:
#             if i == j[0]:
#                 result.append(i)
#     return result


# # Example usage
# # with open("data/phoneme_table.json", "r") as f:
# #     phoneme_table = json.load(f)

# # with open("words.json", "r") as f:
# #     all_words = json.load(f)

# # asr_word = "GINGS"
# # original_possibilities = generate_original_possibilities(
# #     asr_word, phoneme_table, all_words
# # )
# # for i in original_possibilities:
# #     hash_value = hash_word(i)
# #     if hash_value not in all_words:
# #         continue
# #     lst = all_words[hash_value]
# #     for j in lst:
# #         if i == j[0]:
# #             print(i)

# # lst = ["ABC", "DEF"]
# # sentence = " ".join(lst) + "X"
# # print(sentence)

import json
from itertools import product
from hashing import hash_word
from copy import deepcopy


def reverse_phoneme_table(phoneme_table):
    reverse_table = {}
    for original, subs in phoneme_table.items():
        for sub in subs:
            if sub not in reverse_table:
                reverse_table[sub] = []
            reverse_table[sub].append(original)
    return reverse_table


def generate_neighbors(word, reverse_table):
    neighbors = []
    for i, char in enumerate(word):
        if char in reverse_table:
            for original in reverse_table[char]:
                neighbor = word[:i] + original + word[i + 1 :]
                neighbors.append(neighbor)
    return neighbors


def local_beam_search(asr_word, phoneme_table, all_words, beam_width, max_iterations):
    reverse_table = reverse_phoneme_table(phoneme_table)

    # Initialize beam with the original ASR word
    beam = [asr_word]

    for _ in range(max_iterations):
        candidates = []
        for word in beam:
            # Generate neighbors using the reversed phoneme table
            neighbors = generate_neighbors(word, reverse_table)
            candidates.extend(neighbors)

        # Remove duplicates and limit to valid words
        candidates = list(set(candidates))
        valid_candidates = [
            word
            for word in candidates
            if hash_word(word) in all_words
            and any(word == w[0] for w in all_words[hash_word(word)])
        ]

        # If no valid candidates, break the loop
        if not valid_candidates:
            break

        # Sort candidates by their frequency in all_words
        sorted_candidates = sorted(
            valid_candidates,
            key=lambda w: max(
                count for word, count in all_words[hash_word(w)] if word == w
            ),
            reverse=True,
        )

        # Select top beam_width candidates
        beam = sorted_candidates[:beam_width]

    return beam
