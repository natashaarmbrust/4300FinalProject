
# coding: utf-8

# In[1]:

import numpy as np
import json
from .utility import read_file
from stop_words import stop_words
from nltk.corpus import stopwords
total_stopwords=set(stopwords.words('english')).union(set(stop_words))
from .utility import read_file

# In[2]:

data = read_file(22)

#comment comment
# In[3]:

documents = [(x['title'], x['variety'], x['description']) for x in data]


# In[5]:


from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer(stop_words = total_stopwords, max_df = .7, min_df = 75)
my_matrix = vectorizer.fit_transform([x[2] for x in documents]).transpose()

from scipy.sparse.linalg import svds
u, s, v_trans = svds(my_matrix, k=100)


words_compressed, _, docs_compressed = svds(my_matrix, k=40)
docs_compressed = docs_compressed.transpose()

word_to_index = vectorizer.vocabulary_
index_to_word = {i:t for t,i in word_to_index.items()}

# In[17]:

from sklearn.preprocessing import normalize
words_compressed = normalize(words_compressed, axis = 1)


#save words_compressed, word_to_index

def closest_words(word_in, k = 10):
    if word_in not in word_to_index: return "Not in vocab."
    sims = words_compressed.dot(words_compressed[word_to_index[word_in],:])
    asort = np.argsort(-sims)[:k+1]
    return [(index_to_word[i],sims[i]/sims[asort[0]]) for i in asort[1:]]


