import numpy as np
from .utility import read_file


def closest_words(word_in, words_compressed, word_to_index, index_to_word, k = 5):
    if word_in not in word_to_index: return [word_in]
    sims = words_compressed.dot(words_compressed[int(word_to_index[word_in]),:])
    asort = np.argsort(-sims)[:k+1]
    return [index_to_word[str(i)] for i in asort[1:]]


def expand_query(tokens, words_compressed, word_to_index, index_to_word):
    expansion=set()
    for token in tokens:
        expansion.update(closest_words(token, words_compressed, word_to_index, index_to_word))
    print(expansion)

    return " ".join(tokens + list(expansion))
