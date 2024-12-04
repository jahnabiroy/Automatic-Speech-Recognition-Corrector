import csv
import hashlib
import json

def hash_word(word):
    return hashlib.md5(word.encode('utf-8')).hexdigest()

def process_csv_to_json(csv_file, json_file):
    word_list = {}

    # Read the CSV file and append the word and count to a list
    with open(csv_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            word = row['word']
            word = word.strip().upper()
            count = int(row['count'])
            if hash_word(word) not in word_list:
                word_list[hash_word(word)] = []
            word_list[hash_word(word)].append((word, count))

    # Write the hashed data to a JSON file
    with open(json_file, mode='w') as file:
        json.dump(word_list, file, indent=4)


def edit_distance(word1, word2):
    m = len(word1)
    n = len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i  # Deletion cost
    for j in range(n + 1):
        dp[0][j] = j  # Insertion cost
    # Fill the matrix
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]  # No operation needed
            else:
                dp[i][j] = 1 + min(dp[i - 1][j],     # Deletion
                                  dp[i][j - 1],     # Insertion
                                  dp[i - 1][j - 1]) # Substitution
    # The bottom-right cell contains the edit distance
    return dp[m][n]


# Example usage
csv_file = 'data/unigram_freq.csv'  # Replace with your CSV file path
json_file = 'words.json'  # Replace with your JSON file path
process_csv_to_json(csv_file, json_file)
