
# coding: utf-8

# In[1]:

import numpy as np
import json


# In[2]:

data = json.load(open('winemag-data-130k-v2.json'))
print(data[0])


# In[3]:

documents = [(x['title'], x['variety'], x['description']) for x in data]


# In[5]:

from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer(stop_words = 'english', max_df = .7,
                            min_df = 75)
my_matrix = vectorizer.fit_transform([x[2] for x in documents]).transpose()


# In[6]:

print(my_matrix.shape)


# In[7]:

from scipy.sparse.linalg import svds
u, s, v_trans = svds(my_matrix, k=100)


# In[8]:

print(u.shape)
print(s.shape)
print(v_trans.shape)


# In[9]:

import matplotlib
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
plt.plot(s[::-1])
plt.xlabel("Singular value number")
plt.ylabel("Singular value")
plt.show()


# In[10]:

words_compressed, _, docs_compressed = svds(my_matrix, k=40)
docs_compressed = docs_compressed.transpose()


# In[11]:

print(words_compressed.shape)
print(docs_compressed.shape)


# In[16]:

word_to_index = vectorizer.vocabulary_
index_to_word = {i:t for t,i in word_to_index.items()}
print(words_compressed.shape)


# In[17]:

from sklearn.preprocessing import normalize
words_compressed = normalize(words_compressed, axis = 1)


# In[18]:

def closest_words(word_in, k = 10):
    if word_in not in word_to_index: return "Not in vocab."
    sims = words_compressed.dot(words_compressed[word_to_index[word_in],:])
    asort = np.argsort(-sims)[:k+1]
    return [(index_to_word[i],sims[i]/sims[asort[0]]) for i in asort[1:]]


# In[43]:

closest_words("grippy")


# In[25]:

from sklearn.manifold import TSNE
tsne = TSNE(verbose=1)


# In[26]:

print(docs_compressed.shape)
#we'll just take the first 5K documents, because TSNE is memory intensive!
subset = docs_compressed[:5000,:]
projected_docs = tsne.fit_transform(subset)
print(projected_docs.shape)


# In[27]:

plt.figure(figsize=(15,15))
plt.scatter(projected_docs[:,0],projected_docs[:,1])
plt.show()


# In[28]:

from collections import Counter
cats = Counter([x[1] for x in documents])
print(cats)


# In[35]:

from collections import defaultdict
cat_to_color = defaultdict(lambda: 'k')
cat_to_color.update({"Pinot Noir":'g',
               "Chardonnay":'c',
               "Cabernet Sauvignon":'r',
               "Red Blend": "b",
               "Bordeaux-style Red Blend":"y",
               "Riesling":"c",
               "Sauvignon Blanc":"m",
               "Syrah":"y",
               "Rosé":"k",
               "Merlot":"w"})
color_to_project = defaultdict(list)
for i in range(projected_docs.shape[0]):
    color_to_project[cat_to_color[documents[i][1]]].append(i)


# In[34]:

plt.figure(figsize=(15,15))
for color, indices in color_to_project.items():
    indices = np.array(indices)
    plt.scatter(projected_docs[indices,0], projected_docs[indices,1],
                color = color)
plt.show()


# In[36]:

docs_compressed = normalize(docs_compressed, axis = 1)
def closest_wine(project_index_in, k = 5):
    sims = docs_compressed.dot(docs_compressed[project_index_in,:])
    asort = np.argsort(-sims)[:k+1]
    return [(documents[i][0],sims[i]/sims[asort[0]]) for i in asort[1:]]


# In[38]:

for i in range(10):
    print(documents[i][0])
    for title, score in closest_wine(i):
        print("{}:{:.3f}".format(title[:40], score))
    print()


# In[ ]:



