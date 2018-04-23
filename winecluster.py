#elementary clustering
import csv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
from nltk.stem.porter import PorterStemmer
import nltk
import re
import numpy as np
from sklearn.externals import joblib


stemmer=PorterStemmer()

def readcsv(filename):
	data=None
	with open(filename, "r") as file:
		reader=csv.reader(file)
		data=list(reader)
	return data

def build_dict(dat):
	lis=[]
	headers=data[0]
	headers[0]="ID"
	content=data[1::]
	for line in content:
		lis.append(dict(zip(headers,line)))
	return lis

def tokenize_and_stem(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    stems = [stemmer.stem(t) for t in filtered_tokens]
    return stems

data = readcsv("wine_data.csv")
headers=data[0]
content=data[1::]
desc= [x[2] for x in content]
data_dict=build_dict(data)




tfidf_vec=TfidfVectorizer(stop_words="english", max_features=200000,max_df=.8, min_df=.005, norm="l2")
doc_by_vocab = tfidf_vec.fit_transform([d['description'] for d in data_dict]).toarray()
index_to_vocab = {i:v for i, v in enumerate(tfidf_vec.get_feature_names())}

true_k = 10
model = KMeans(n_clusters=true_k, init='k-means++', max_iter=50, n_init=1)
model.fit(doc_by_vocab)

print("Top terms per cluster:")
order_centroids = model.cluster_centers_.argsort()[:, ::-1]
terms = tfidf_vec.get_feature_names()
for i in range(true_k):
    print ("Cluster %d:" % i,)
    for ind in order_centroids[i, :10]:
        print (' %s' % terms[ind],)
joblib.dump(model,  'doc_cluster.pkl')

clusters = model.labels_.tolist()
print(clusters)
