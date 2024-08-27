import json
from helper import generate_original_possibilities
class Agent(object):
    def __init__(self, phoneme_table, vocabulary,word_file = "words.json") -> None:
        """
        Your agent initialization goes here. You can also add code but don't remove the existing code.
        """
        self.phoneme_table = phoneme_table
        self.vocabulary = vocabulary
        self.best_state = None
        with open(word_file, 'r') as f:
            self.word_file = json.load(f)

    def asr_corrector(self, environment):
        """
        Your ASR corrector agent goes here. Environment object has the following important members.
        - environment.init_state: Initial state of the environment. This is the text that needs to be corrected.
        - environment.compute_cost: A cost function that takes a text and returns a cost. E.g., environment.compute_cost("hello") -> 0.5

        Your agent must update environment.best_state with the corrected text discovered so far.
        """
        self.best_state = environment.init_state
        current_cost = environment.compute_cost(self.best_state)
        words = self.best_state.split()
        print(self.best_state)
        print()

        def compute_cost_lst(lst):
            sentence = " ".join(lst)
            return environment.compute_cost(sentence)

        temp_lst = words.copy()

        f = True
        while(f):
            f = False
            for i in range(len(temp_lst)):
                asr_word = temp_lst[i]
                original_possibilities = generate_original_possibilities(asr_word, self.phoneme_table, self.word_file)
                for possibility in original_possibilities:
                    # Temporarily replace the word and compute the new cost
                    words[i] = possibility
                    new_cost = compute_cost_lst(words)
                    # Update if the new cost is lower
                    if new_cost < current_cost:
                        f = True
                        current_cost = new_cost
                        self.best_state = " ".join(words)
                    else:
                        # Revert if no improvement
                        words[i] = asr_word



        print(self.best_state)
