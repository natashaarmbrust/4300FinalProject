import csv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
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

data = pd.read_csv("../data/wine-reviews/winemag-data-130k-v2.csv")

total_stop_words = set(stopwords.words('english')).union(set(stop_words))

tfidf_vec = TfidfVectorizer(stop_words=total_stop_words, max_features=200000,max_df=.3, min_df=.005, norm="l2")

doc_by_vocab = tfidf_vec.fit_transform(data['description']).toarray()

index_to_vocab = {i:v for i, v in enumerate(tfidf_vec.get_feature_names())}

true_k = 9
model = KMeans(n_clusters=true_k, init='k-means++', max_iter=50, n_init=1)
model.fit(doc_by_vocab)

print("Top terms per cluster:")
order_centroids = model.cluster_centers_.argsort()[:, ::-1]
terms = tfidf_vec.get_feature_names()
for i in range(true_k):
    print("Cluster %d:" % i),
    for ind in order_centroids[i, :20]:
        print(' %s' % terms[ind]), 
    print("\n")
