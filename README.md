# Automatic Speech Recognition Corrector

This assignment was done as part of COL333 Course Requirements.

This report outlines the development of an Automatic Speech Recognition (ASR) corrector utilizing a local beam search strategy to improve the text outputs from ASR systems. The approach focuses on minimizing errors by leveraging phoneme mappings, word frequencies, and dynamic programming techniques. Below, we provide a detailed overview of the core algorithm and its key components.

## Core Algorithm Overview

The ASR corrector is designed around the `Agent` class, which is initialized with several parameters, including a phoneme table, a vocabulary list, beam width, maximum iterations, and a small threshold (`epsilon`) to fine-tune cost improvements. The goal is to iteratively refine the initial ASR output to minimize correction costs.

### Key Components and Methods:

1. **Hashing and Phoneme Mapping**:

   - `hash_word` Function: Generates a unique hash (using MD5) for each word, allowing for efficient lookups in `word_file`, a dictionary containing words and their frequency counts indexed by hashed values.
   - `reverse_phoneme_table` Function: Creates a reverse mapping of phonemes to their potential original forms, which aids in generating possible word corrections based on phonetic similarities.

2. **Search Functions**:

   - `my_search`: Identifies potential corrections for words by exploring phoneme substitutions using the reverse phoneme table.
   - `local_beam_search`: Narrows down the search to the most probable corrections, constrained by a specified beam width. This function prioritizes words with higher frequency counts, improving the likelihood of selecting the correct word.

3. **Text Correction**:

   - `replace_after` Function: Utilizes regular expressions to apply standard corrections, such as substituting 'Z' with 'S' or 'D' with 'ED' to rectify common ASR errors.

4. **Iterative Improvement**:

   - The algorithm operates in a loop, continuously testing potential corrections by replacing words one at a time. Each iteration involves recalculating the overall cost and updating the best state whenever a lower-cost configuration is found.
   - Words are replaced using alternatives suggested by the `local_beam_search` function, ensuring a focus on minimizing correction costs.

5. **Addition of Leading and Trailing Words**:

   - The approach also considers adding leading or trailing words from the vocabulary to find configurations that further reduce the overall sentence cost.

6. **Cost Evaluation**:

   - `compute_cost_lst` Function: Calculates the cost of a given list of words, providing a metric to evaluate the quality of corrections based on the environment's cost function.

7. **Handling Proper Nouns**:

   - When the corrector encounters a proper noun that is not present in the vocabulary or fails to match any valid English word, it attempts substitutions with words that have an edit distance below a specific threshold. This strategy ensures that even unique or uncommon names are handled accurately without being incorrectly replaced by more common words.

## Core Ideas

- **_Beam Search Strategy_**: The core algorithm employs a local beam search to manage the correction process, maintaining a limited set of candidate solutions at each step to avoid a costly exhaustive search.

- **_Phoneme-Based Correction_**: By utilizing phoneme mappings, the system can explore corrections that are linguistically plausible, thereby enhancing the accuracy of the corrections.

- **_Dynamic Programming for Substitution_**: The algorithm leverages dynamic programming to efficiently determine potential substitutions for each word, utilizing phonetic similarity and edit distance constraints.

- **_Cost-Driven Iterative Refinement_**: The iterative process focuses on testing replacements and recalculating costs to ensure that only beneficial corrections are retained.

- **_Hashing for Efficient Lookup_**: Hashing each word enables rapid verification against a precompiled list of valid English words, optimizing the correction process's performance.

- **_Handling Proper Nouns_**: When no valid English words are found, the system attempts substitutions based on words with an edit distance below a certain threshold, specifically targeting proper nouns that may not match standard vocabulary lists.

## Conclusion

The ASR corrector designed in this assignment effectively combines beam search, phoneme mapping, dynamic programming, and hashing techniques to iteratively refine ASR outputs. By focusing on minimizing correction costs and optimizing the search space, this approach is adaptable for use with various cost functions and models. Reversing the phoneme table and leveraging a comprehensive word-frequency dictionary further enhances the system's ability to identify the best possible corrections, thereby improving the overall accuracy of ASR systems.

## Contributors 

- [Jahnabi Roy](https://github.com/jahnabiroy)
- [Abhinav Rajesh Shripad](https://github.com/33Arsenic75)
