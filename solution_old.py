class Agent(object):
    def __init__(self, phoneme_table, vocabulary) -> None:
        """
        Your agent initialization goes here. You can also add code but don't remove the existing code.
        """
        self.phoneme_table = phoneme_table
        self.vocabulary = vocabulary
        self.best_state = None

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

        # Function to generate candidates by replacing phonemes in a specific word
        def generate_word_candidates(word):
            candidates = set()
            for phoneme, subs in self.phoneme_table.items():
                if phoneme in word:
                    for sub in subs:
                        new_word = word.replace(phoneme, sub)
                        candidates.add(new_word)
            return candidates

        # Function to generate candidates by adding missing vocabulary words
        def generate_missing_word_candidates(word):
            candidates = set()
            # Add each vocabulary word before and after the current word
            for vocab_word in self.vocabulary:
                candidates.add(vocab_word + " " + word)
                candidates.add(word + " " + vocab_word)
            return candidates

        # Local search for each word in the text
        for i in range(len(words)):
            best_word = words[i]
            best_word_cost = current_cost

            # Generate all possible candidates for the current word
            word_candidates = generate_word_candidates(words[i])
            missing_word_candidates = generate_missing_word_candidates(words[i])

            # Evaluate each candidate for the current word position
            for candidate_word in word_candidates | {words[i]}:
                # Form a new sentence with the candidate word
                new_sentence = " ".join(words[:i] + [candidate_word] + words[i+1:])
                candidate_cost = environment.compute_cost(new_sentence)

                # If a better candidate is found, update the best word and cost
                if candidate_cost < best_word_cost:
                    best_word = candidate_word
                    best_word_cost = candidate_cost

            # Evaluate candidates with missing words
            for candidate_sentence in missing_word_candidates:
                # Create new sentence and compute cost
                candidate_cost = environment.compute_cost(candidate_sentence)

                # If a better candidate is found, update the best state and cost
                if candidate_cost < current_cost:
                    self.best_state = candidate_sentence
                    current_cost = candidate_cost
                    words = self.best_state.split()  # Update words with the new best state
                    break

            # Update the word in the sentence if a better candidate was found
            if best_word != words[i]:
                words[i] = best_word
                current_cost = best_word_cost

        # Update the best state in the environment
        self.best_state = " ".join(words)
        environment.best_state = self.best_state
        print(self.best_state, current_cost)
