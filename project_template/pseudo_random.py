import random
import numpy as np
import json
from scipy.sparse.linalg import svds
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize
# import matplotlib
# import numpy as np
# import matplotlib.pyplot as plt

data = json.load(open('winemag-data-130k-v2.json'))
documents = [(x['title'], x['variety'], x['description']) for x in data]
vectorizer = TfidfVectorizer(stop_words = 'english', max_df = .7,
                            min_df = 75)
my_matrix = vectorizer.fit_transform([x[2] for x in documents]).transpose()
u, s, v_trans = svds(my_matrix, k=100)
# get_ipython().run_line_magic('matplotlib', 'inline')
# plt.plot(s[::-1])
# plt.xlabel("Singular value number")
# plt.ylabel("Singular value")
# plt.show()

words_compressed, _, docs_compressed = svds(my_matrix, k=40)
docs_compressed = docs_compressed.transpose()
word_to_index = vectorizer.vocabulary_
index_to_word = {i:t for t,i in word_to_index.items()}

words_compressed = normalize(words_compressed, axis = 1)

def closest_words(word_in, k = 10):
    if word_in not in word_to_index: return "Not in vocab."
    sims = words_compressed.dot(words_compressed[word_to_index[word_in],:])
    asort = np.argsort(-sims)[:k+1]
    return [(index_to_word[i],sims[i]/sims[asort[0]]) for i in asort[1:]]

def get_index(query):
	random.seed(len(query))
	return random.randint(0, 2)

def expand_query(query, word_list):
	idx = get_index(query)
	to_expand = word_list[idx:][::3]
	expanded = [closest_words(word) for word in to_expand]

	return word_list + expanded

print(expand_query('cabernet', ['cabernet','sauvignon','bordeaux','red','tannin']))