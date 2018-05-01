import json
import csv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score, silhouette_score
from nltk.stem.porter import PorterStemmer
import nltk
from nltk.corpus import stopwords
import re
import numpy as np
from sklearn.externals import joblib
import pandas as pd
from collections import Counter
import spacy
nlp = spacy.load('en')
from stop_words import stop_words
data=[]
total_stop_words = set(stopwords.words('english')).union(set(stop_words))
with open("../data/wine-reviews/final_wines_data.json") as data_file:    
    data = json.load(data_file)

total_stop_words = set(stopwords.words('english')).union(set(stop_words))

# def wine_profile(description):

#     stop_words=total_stop_words
#     doc=nlp(description.lower())
#     wordset=set()
#     chunks=[chunk.text for chunk in doc.noun_chunks]
#     remove_tags={"CD" , "RB", "VBZ", "VBD", "IN", "MD", "VBG", "VBP","PUNCT"}
#     for token in doc:
#         if(token.pos_ not in remove_tags and not token.is_stop):
#             wordset.add(token.lemma_)

#     wordset.update(chunks)
#     return wordset-stop_words



tfidf_vec = TfidfVectorizer(stop_words=total_stop_words, max_features=200000,max_df=.3, min_df=.005, norm="l2")


print("running")
doc_by_vocab = tfidf_vec.fit_transform([" ".join(set(d['profile'])-total_stop_words) for d in data]).toarray()
clusters=[]

index_to_vocab = {i:v for i, v in enumerate(tfidf_vec.get_feature_names())}
print("running")
true_k = 16
model = KMeans(n_clusters=true_k, init='k-means++', max_iter=50, n_init=1)
model.fit(doc_by_vocab)
print("running")
print("Top terms per cluster:")
order_centroids = model.cluster_centers_.argsort()[:, ::-1]
terms = tfidf_vec.get_feature_names()
dictionary = {}
for i in range(true_k):
    print("Cluster %d:" % i),
    dictionary[i] = []
    for ind in order_centroids[i, :100]:
        dictionary[i].append(terms[ind])

print(model.labels_)
# print(silhouette_score(doc_by_vocab, model.labels_))

with open("cluster_labels2.csv", 'w') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(model.labels_)

with open('words.txt', 'w') as outfile:
    json.dump(dictionary, outfile)
