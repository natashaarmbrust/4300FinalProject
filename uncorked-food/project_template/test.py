from .models import Docs
import os
import Levenshtein
import json
import re
import numpy as np
from collections import defaultdict
from collections import Counter
import math


def tokenize(text):
	"""Returns a list of words that make up the text.

    Note: for simplicity, lowercase everything.
    Requirement: Use Regex to satisfy this function

    Params: {text: String}
    Returns: Array
    """

	tokenized_text = text.lower()
	tokenized_text = re.findall(r'[a-z0-9]+',
								tokenized_text)  # splits string with delimiter being everything except alphabetical letters
	return tokenized_text

def read_file(n):
	path = Docs.objects.get(id = n).address;
	file = open(path)
	transcripts = json.load(file)
	return transcripts

wine_data = read_file(4)

def _edit(query, msg):
    return Levenshtein.distance(query.lower(), msg.lower())


def build_inverted_index(msgs):
	inverted_index = defaultdict(dict)
	doc_idx = 0
	docid_to_winetitle = dict()
	for wine in msgs:
		s = ' '
		string_list = [wine['title'],wine['variety'],wine['region_1'],wine['province'],wine['country'],wine['winery'],wine['description']]
		wine_tokens = tokenize(s.join(filter(None, string_list)))
		for word in wine_tokens:
			if word not in inverted_index:
				inverted_index[word][str(doc_idx)] = 1
			elif str(doc_idx) not in inverted_index[word]:
				inverted_index[word][str(doc_idx)] = 1
			else:
				inverted_index[word][str(doc_idx)] += 1
		docid_to_winetitle[doc_idx] = wine['title']
		doc_idx += 1

	for word in inverted_index:
		inverted_index[word] = inverted_index[word].items()
	return inverted_index, docid_to_winetitle



def compute_idf(inv_idx, n_docs, min_df=10, max_df_ratio=0.95):

	IDF_dict = dict()
	for word in inv_idx:
		DF_word = len(inv_idx[word])

		if DF_word >= min_df and DF_word / n_docs <= max_df_ratio:
			IDF_dict[word] = math.log2(n_docs / (1 + DF_word))

	return IDF_dict




def compute_doc_norms(index, idf, n_docs):

	doc_norms = np.zeros(n_docs)
	for word in index:
		for doc_id in index[word]:
			if word in idf:
				doc_norms[int(doc_id[0])] += (int(doc_id[1]) * idf[word]) ** 2

	doc_norms1 = np.sqrt(doc_norms)
	return doc_norms1

global_inverted_index, docid_to_wine_title = build_inverted_index(wine_data)
num_docs = len(wine_data)
idf_dict = compute_idf(global_inverted_index, num_docs)
doc_norms = compute_doc_norms(global_inverted_index, idf_dict, num_docs)



def index_search_cosine_sim(query):#index idf doc_norms


	query = tokenize(query.lower())
	score_query_doc = dict()
	query_norm = 0
	for word in query:
		if word in idf_dict:
			query_norm += idf_dict[word] ** 2
			for doc in global_inverted_index[word]:
				if doc[0] not in score_query_doc:
					score_query_doc[doc[0]] = idf_dict[word] * doc[1] * idf_dict[word]
				else:
					score_query_doc[doc[0]] += idf_dict[word] * doc[1] * idf_dict[word]

	query_norm = np.sqrt(query_norm)
	for doc in score_query_doc:
		score_query_doc[doc] = score_query_doc[doc] / (query_norm * doc_norms[int(doc)])

	sorted_by_second = sorted(list(score_query_doc.items()), key=lambda tup: tup[1], reverse=True)
	final = [(v, docid_to_wine_title[int(k)]) for k, v in sorted_by_second]
	return final[:10]

def find_similar_levenshtein(query):
	# wine_data = read_file(4)
	result = []
	for wine in wine_data:
		# for item in transcript:
			wine_description = wine['description']
			wine_description_tokenized = tokenize(wine_description)
			result.append(((_edit(query, wine_description)), wine_description,wine['title']))

	top_ten = sorted(result, key=lambda tup: tup[0])[:10]
	final = []
	for i in top_ten:
		final.append(i[2])

	return final

