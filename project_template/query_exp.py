import numpy as np
from .utility import read_file

# food_words_compressed = read_file()
# food_word_to_index = read_file()
# food_index_to_word = read_file()


# wine_words_compressed = read_file()
# wine_word_to_index = read_file()
# wine_index_to_word = read_file()

def closest_words(word_in, words_compressed, word_to_index, index_to_word, k = 3):
    if word_in not in word_to_index: return 
    sims = words_compressed.dot(words_compressed[word_to_index[word_in],:])
    asort = np.argsort(-sims)[:k+1]
    return [(index_to_word[i],sims[i]/sims[asort[0]]) for i in asort[1:]]


def expand_query(tokens, words_compressed, word_to_index, index_to_word):
	expansion=set()
	for token in tokens:
		expansion.update(closest_words(token, words_compressed, word_to_index, index_to_word))

	return " ".join(tokens + list(expansion))
