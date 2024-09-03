from itertools import product
import json
from hashing import hash_word

# import re
# def replace_after(text):
#     # Define patterns and replacements
#     replacements = {
#         r"'Z": "'S",  # Replace 'Z' with 'S' when preceded by a comma
#         r"'D": "'ED", # Replace 'D' with 'ED' when preceded by a comma
#         # Add more rules here if needed
#     }

#     # Apply each replacement
#     for pattern, replacement in replacements.items():
#         text = re.sub(pattern, replacement, text)

#     return text
#
def reverse_phoneme_table(phoneme_table):
    reverse_table = {}
    for original, subs in phoneme_table.items():
        for sub in subs:
            if sub not in reverse_table:
                reverse_table[sub] = []
            reverse_table[sub].append(original)
    return reverse_table



def my_search(asr_word, phoneme_table):
    reverse_table = reverse_phoneme_table(phoneme_table)
    for c in (chr(i) for i in range(ord('A'), ord('Z') + 1)):
        if c not in reverse_table:
            reverse_table[c] = []
        reverse_table[c].append(c)

    for k in reverse_table.keys():
        reverse_table[k].append(k)
        reverse_table[k] = list(set(reverse_table[k]))

    keys = list(reverse_table.keys())
    lst = [[] for i in range(len(asr_word))]
    lst[0]=[""]
    for i in range(len(asr_word)):
        if(len(lst[0])>1) and "" in lst[0]:
            lst[0].remove("")
        for k in keys:
            if(len(lst[0])>1) and "" in lst[0]:
                lst[0].remove("")
            if k == asr_word[i:i+len(k)]:
                if(i ==0):
                    for add in reverse_table[k]:
                        lst[i + len(k) - 1].append(add)

                else:
                    for pre in lst[i-1]:
                        for add in reverse_table[k]:
                            lst[i + len(k) - 1].append(pre + add)
    for i in lst:
        print(i)
    if("THERE'S") in lst[-1]:
        print("YES")
    return list(set(lst[-1]))



def local_beam_search(asr_word, phoneme_table, all_words, beam_width):
    possible_words = my_search(asr_word, phoneme_table)
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

all_words = json.load(open('words.json'))
phoneme_table = json.load(open('data/phoneme_table.json'))
phoneme_table["'"]=["'"]
asr_word = "THARC"
beam_width = 50
print(local_beam_search(asr_word, phoneme_table, all_words, beam_width))


# import re
# sentence = "example's state here"
# words = re.split(r"( |')", sentence)
# words = [word for word in words if word and word != " "]

# print(words)
# def custom_join(words):
#     # Initialize an empty string to store the result
#     result = ""

#     for i, word in enumerate(words):
#         # If the word is an apostrophe, do not add a space before it
#         if word == "'":
#             result += "'"
#         else:
#             # If the previous word is an apostrophe, don't add a space
#             if i > 0 and words[i - 1] == "'":
#                 result += word
#             else:
#                 # Add a space before the word if it's not the first word
#                 if i > 0:
#                     result += " "
#                 result += word

#     return result
# print(custom_join(words))
