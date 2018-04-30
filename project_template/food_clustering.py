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
from food_stopwords import stop_words
nlp = spacy.load('en')
total_stopwords=set(stopwords.words('english')).union(set(stop_words))

data = pd.read_json("../data/epicurious-recipes-with-rating-and-nutrition/full_format_recipes.json")

tfidf_vec = TfidfVectorizer(stop_words=total_stopwords,  max_features=200000,max_df=.3, min_df=.005, norm="l2")

cats = data['categories'].as_matrix()
for i in range(len(cats)):
    cat = cats[i]
    if type(cat) == list:
        cats[i] = " ".join(cat) # make lists into strings for input to vectorizer
    else:
        cats[i] = "" # in the case of nan 

doc_by_vocab = tfidf_vec.fit_transform(cats).toarray()

index_to_vocab = {i:v for i, v in enumerate(tfidf_vec.get_feature_names())}

true_k = 30
model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
model.fit(doc_by_vocab)

print("Top terms per cluster:")
order_centroids = model.cluster_centers_.argsort()[:, ::-1]
terms = tfidf_vec.get_feature_names()
for i in range(true_k):
    print("Cluster %d:" % i),
    for ind in order_centroids[i, :50]:
        print(' %s' % terms[ind]), 
    print("\n")
print(model.labels_)
# print(silhouette_score(doc_by_vocab, model.labels_))

# with open("food_cluster_labels.csv", 'w') as myfile:
#     wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
#     wr.writerow(model.labels_)
