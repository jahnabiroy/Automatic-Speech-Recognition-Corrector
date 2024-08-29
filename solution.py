# import json
# from helper import generate_original_possibilities


# class Agent(object):
#     def __init__(self, phoneme_table, vocabulary, word_file="words.json") -> None:
#         """
#         Your agent initialization goes here. You can also add code but don't remove the existing code.
#         """
#         self.phoneme_table = phoneme_table
#         self.vocabulary = vocabulary
#         self.best_state = None
#         with open(word_file, "r") as f:
#             self.word_file = json.load(f)

#     def asr_corrector(self, environment):
#         """
#         Your ASR corrector agent goes here. Environment object has the following important members.
#         - environment.init_state: Initial state of the environment. This is the text that needs to be corrected.
#         - environment.compute_cost: A cost function that takes a text and returns a cost. E.g., environment.compute_cost("hello") -> 0.5

#         Your agent must update environment.best_state with the corrected text discovered so far.
#         """
#         self.best_state = environment.init_state
#         current_cost = environment.compute_cost(self.best_state)
#         words = self.best_state.split()
#         print(self.best_state)
#         print()

#         def compute_cost_lst(lst):
#             sentence = " ".join(lst)
#             return environment.compute_cost(sentence)

#         temp_lst = words.copy()

#         f = True
#         while f:
#             f = False
#             for i in range(len(temp_lst)):
#                 asr_word = temp_lst[i]
#                 original_possibilities = generate_original_possibilities(
#                     asr_word, self.phoneme_table, self.word_file
#                 )
#                 for possibility in original_possibilities:
#                     # Temporarily replace the word and compute the new cost
#                     words[i] = possibility
#                     new_cost = compute_cost_lst(words)
#                     # Update if the new cost is lower
#                     if new_cost < current_cost:
#                         f = True
#                         current_cost = new_cost
#                         self.best_state = " ".join(words)
#                     else:
#                         # Revert if no improvement
#                         words[i] = asr_word

#         print(self.best_state)

import json
from helper import local_beam_search


class Agent(object):
    def __init__(
        self,
        phoneme_table,
        vocabulary,
        word_file="words.json",
        beam_width=5,
        max_iterations=15,
        window_size=3,
    ) -> None:
        """
        Agent initialization with local beam search parameters and sliding window.
        """
        self.phoneme_table = phoneme_table
        self.vocabulary = vocabulary
        self.best_state = None
        self.beam_width = beam_width
        self.max_iterations = max_iterations
        self.window_size = window_size
        with open(word_file, "r") as f:
            self.word_file = json.load(f)

    def asr_corrector(self, environment):
        """
        ASR corrector agent using local beam search with sliding window.
        """
        self.best_state = environment.init_state
        current_cost = environment.compute_cost(self.best_state)
        words = self.best_state.split()
        print("Initial state:", self.best_state)
        print("Initial cost:", current_cost)

        def compute_cost_lst(lst):
            sentence = " ".join(lst)
            return environment.compute_cost(sentence)

        improved = True
        while improved:
            improved = False
            for i in range(len(words) - self.window_size + 1):
                window = words[i : i + self.window_size]
                original_window = window.copy()

                # Generate candidates for each word in the window
                candidates = [
                    local_beam_search(
                        word,
                        self.phoneme_table,
                        self.word_file,
                        self.beam_width,
                        self.max_iterations,
                    )
                    for word in window
                ]

                # Generate all combinations of candidates
                import itertools

                combinations = list(itertools.product(*candidates))

                best_combination = window
                best_combination_cost = current_cost

                for combination in combinations:
                    words[i : i + self.window_size] = combination
                    new_cost = compute_cost_lst(words)
                    if new_cost < best_combination_cost:
                        best_combination = list(combination)
                        best_combination_cost = new_cost

                if best_combination != original_window:
                    improved = True
                    words[i : i + self.window_size] = best_combination
                    current_cost = best_combination_cost
                    self.best_state = " ".join(words)
                else:
                    words[i : i + self.window_size] = original_window

        print("Final state:", self.best_state)
        print("Final cost:", current_cost)
