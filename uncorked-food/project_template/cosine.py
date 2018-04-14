from .models import Docs
import os
import Levenshtein
import json
import re
import numpy as np
from collections import defaultdict
from collections import Counter
import math
from enum import Enum
from utility import *
from .wine_processing import build_inverted_index_wine
from .food_processing import build_inverted_index_food

class SearchType(Enum):
    FOOD = 1
    WINE = 2 

def search(query, searchType):
  output = ""

  if searchType == SearchType.WINE:
    wine_data = read_file(4)
    inverted_index, docid_to_wine_title = build_inverted_index_wine(wine_data)
    num_docs = len(wine_data)
    idf_dict = compute_idf(inverted_index, num_docs)
    doc_norms = compute_doc_norms(inverted_index, idf_dict, num_docs)
    output = index_search_cosine_sim(query, inverted_index, doc_norms, idf_dict, docid_to_wine_title)

  elif searchType == SearchType.FOOD:
    food_data = read_csv("./data/epicurious-recipes-with-rating-and-nutrition/epi_r.csv")
    inverted_index, recipe_id_to_title = build_inverted_index_food(food_data)
    num_docs = len(food_data)
    idf_dict = compute_idf(inverted_index, num_docs)
    doc_norms = compute_doc_norms(inverted_index, idf_dict, num_docs)
    output = index_search_cosine_sim(query, inverted_index, doc_norms, idf_dict, recipe_id_to_title)
  
  return output 



## MARK - Cosine Similarity 

def compute_idf(inv_idx, n_docs, min_df=10, max_df_ratio=0.95):
  IDF_dict = dict()
  for word in inv_idx:
    DF_word = len(inv_idx[word])

    if DF_word >= min_df and DF_word / n_docs <= max_df_ratio:
      IDF_dict[word] = math.log(n_docs / (1 + DF_word))

  return IDF_dict

def compute_doc_norms(index, idf, n_docs):
  doc_norms = np.zeros(n_docs)
  for word in index:
    for doc_id in index[word]:
      if word in idf:
        doc_norms[int(doc_id[0])] += (int(doc_id[1]) * idf[word]) ** 2

  doc_norms1 = np.sqrt(doc_norms)
  return doc_norms1

def index_search_cosine_sim(query, inverted_index, doc_norms, idf, index_to_title):
    query = tokenize(query.lower())
    score_query_doc = dict()
    query_norm = 0
    for word in query:
        if word in idf:
            query_norm += idf[word] ** 2
            for doc in inverted_index[word]:
                if doc[0] not in score_query_doc:
                    score_query_doc[doc[0]] = idf[word] * idf[word] * doc[1]
                else:
                    score_query_doc[doc[0]] += idf[word] * idf[word] * doc[1]

    query_norm = np.sqrt(query_norm)
    for doc in score_query_doc:
        score_query_doc[doc] = score_query_doc[doc] / (query_norm * doc_norms[int(doc)])

    sorted_by_second = sorted(list(score_query_doc.items()), key=lambda tup: tup[1], reverse=True)
    final = [(v, index_to_title[int(k)]) for k, v in sorted_by_second]
    return final[:10]


### MARK - Levenshtein

def _edit(query, msg):
    return Levenshtein.distance(query.lower(), msg.lower())

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