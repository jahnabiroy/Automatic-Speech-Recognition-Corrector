from hashing import hash_word, process_csv_to_json, edit_distance
import json

def replace(string, what, replacement, occurrence=1):
    start_index = -1
    current_occurrence = 0
    for _ in range(occurrence):
        start_index = string.find(what, start_index + 1)
        if start_index == -1:
            return string
    if start_index != -1:
        return string[:start_index] + replacement + string[start_index + len(what):]
    else:
        return string

def score_words(dist,freq):
    return freq - dist

def correct_word(word,file):
    hash_value = hash_word(word)
    with open(file, mode='r') as file:
        data = json.load(file)
        min_score = float('inf')
        correct_word = ''
        for key in data:
            distance = edit_distance(word, data[key]['word'])
            frq = data[key]['count']
            # if(distance==1):
            #     print(data[key]['word'])
            if score_words(distance,frq) <= min_score:
                min_score = score_words(distance,frq)
                correct_word = data[key]['word']
        return correct_word

print(correct_word("EOY", "words.json"))
print(edit_distance("EOY", "BOY"))
