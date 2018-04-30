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

data = pd.read_csv("../data/wine-reviews/winemag-data-130k-v2.csv")

total_stop_words = set(stopwords.words('english')).union(set(stop_words))

def wine_profile(description):

    stop_words=set(stopwords.words('english'))
    doc=nlp(description.lower())
    wordset=set()
    chunks=[chunk.text for chunk in doc.noun_chunks]
    remove_tags={"CD" , "RB", "VBZ", "VBD", "IN", "MD", "VBG", "VBP","PUNCT"}
    for token in doc:
        if(token.pos_ not in remove_tags and not token.is_stop):
            wordset.add(token.lemma_)
    chunkwords=set()

    wordset.update(chunks)
    return wordset-stop_words


tfidf_vec = TfidfVectorizer(tokenizer=wine_profile, max_features=200000,max_df=.3, min_df=.005, norm="l2")

doc_by_vocab = tfidf_vec.fit_transform(data['description']).toarray()

index_to_vocab = {i:v for i, v in enumerate(tfidf_vec.get_feature_names())}

true_k = 16
model = KMeans(n_clusters=true_k, init='k-means++', max_iter=50, n_init=1)
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

with open("cluster_labels.csv", 'w') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(model.labels_)
