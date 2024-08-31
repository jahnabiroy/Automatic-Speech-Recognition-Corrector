import json
from hashing import hash_word
from helper import local_beam_search
import re


def replace_after(text):
    # Define patterns and replacements
    replacements = {
        r"'Z": "'S",  # Replace 'Z' with 'S' when preceded by a comma
        r"'D": "ED",  # Replace 'D' with 'ED' when preceded by a comma
        # Add more rules here if needed
    }

    # Apply each replacement
    for pattern, replacement in replacements.items():
        text = re.sub(pattern, replacement, text)

    return text


class Agent(object):
    def __init__(
        self,
        phoneme_table,
        vocabulary,
        word_file="words.json",
        beam_width=25,
        max_iterations=15,
        epsilon=1e-5,
    ) -> None:
        """
        Agent initialization with local beam search parameters and sliding window.
        """
        self.phoneme_table = phoneme_table
        self.vocabulary = vocabulary
        self.best_state = None
        self.beam_width = beam_width
        self.max_iterations = max_iterations
        self.epsilon = epsilon
        with open(word_file, "r") as f:
            self.word_file = json.load(f)

    def asr_corrector(self, environment):
        """
        Your ASR corrector agent goes here. Environment object has the following important members.
        - environment.init_state: Initial state of the environment. This is the text that needs to be corrected.
        - environment.compute_cost: A cost function that takes a text and returns a cost. E.g., environment.compute_cost("hello") -> 0.5

        Your agent must update environment.best_state with the corrected text discovered so far.
        """
        self.best_state = environment.init_state
        self.best_state = replace_after(self.best_state)
        current_cost = environment.compute_cost(self.best_state)
        words = self.best_state.split()

        def compute_cost_lst(lst):
            sentence = " ".join(lst)
            return environment.compute_cost(sentence)

        temp_lst = words.copy()
        possible_changes = [[] for _ in range(len(temp_lst))]
        for i in range(len(temp_lst)):
            possible_changes[i] = local_beam_search(
                temp_lst[i],
                self.phoneme_table,
                self.word_file,
                self.beam_width,
            )

        f = True
        while f:
            f = False
            for i in range(len(temp_lst)):
                test = words.copy()
                asr_word = temp_lst[i]
                original_possibilities = possible_changes[i]
                for possibility in original_possibilities:
                    # Temporarily replace the word and compute the new cost
                    test[i] = possibility
                    new_cost = compute_cost_lst(test)
                    # Update if the new cost is lower
                    if new_cost < current_cost:
                        f = True
                        current_cost = new_cost
                        words = test.copy()
                        self.best_state = " ".join(words)

        leading_trailing_words = self.vocabulary
        word_file = self.word_file

        def func(x):
            hash_value = hash_word(x)
            if hash_value not in word_file:
                return 0
            lst = word_file[hash_value]
            for j in lst:
                if x == j[0]:
                    return j[1]
            return 0

        leading_trailing_words = sorted(
            leading_trailing_words, key=lambda x: func(x), reverse=True
        )

        epsilon = self.epsilon
        for lead in leading_trailing_words:
            test = [lead] + words
            new_cost = compute_cost_lst(test)
            if new_cost < current_cost - epsilon:
                current_cost = new_cost
                self.best_state = " ".join(test)

        for trail in leading_trailing_words:
            test = words + [trail]
            new_cost = compute_cost_lst(test)
            if new_cost < current_cost - epsilon:
                current_cost = new_cost
                self.best_state = " ".join(test)

        print(self.best_state)
