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
import os
# import nltk
# import spacy
# nltk.download('stopwords')
# nltk.download('averaged_perceptron_tagger')
# from nltk.corpus import stopwords
# nlp = spacy.load('en')
# from stop_words import stop_words


from .utility import read_file,read_csv,tokenize
from .wine_processing import build_inverted_index_wine
from .food_processing import build_inverted_index_food
from .mapping import generate_food_words

## MARK - Cosine Similarity

def compute_idf(inv_idx, n_docs, min_df=0, max_df_ratio=1):
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

def index_search_cosine_sim_food(query, inverted_index, doc_norms, idf, raw_food_data):
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

    food_output = []
    num = min(len(score_query_doc), 10)
    for i in range(num):
        doc_id = sorted_by_second[i][0]
        doc_score = sorted_by_second[i][1]

        title = raw_food_data[int(doc_id)]['title']
        ingredients = raw_food_data[int(doc_id)]['ingredients']
        directions = raw_food_data[int(doc_id)]['directions']
        calories = raw_food_data[int(doc_id)]['calories']
        rating = raw_food_data[int(doc_id)]['rating']
        categories = raw_food_data[int(doc_id)]['categories']

        food_output.append(
            {'categories':categories,'rating':rating,'calories':calories, 'title': title,'ingredients':ingredients,'directions':directions})
    return food_output
    # final = [{"title": index_to_title[str(k)]} for k, v in sorted_by_second]
    #
    # return final[:10]

# def wine_profile(description):
    
#     total_stop_words=set(stopwords.words('english')).union(set(stop_words))
#     doc=nlp(description.lower())
#     wordset=set()
#     chunks=[chunk.text for chunk in doc.noun_chunks]
#     remove_tags={"CD" , "RB", "VBZ", "VBD", "IN", "MD", "VBG", "VBP","PUNCT"}
#     for token in doc:
#         if(token.pos_ not in remove_tags and not token.is_stop):
#             wordset.add(token.lemma_)
#     chunkwords=set()

#     wordset.update(chunks)
#     return wordset-total_stop_words
  
def index_search_cosine_sim_wine(query, inverted_index, doc_norms, idf, raw_wine_data):

    query = tokenize(query.lower())
    score_query_doc = dict()
    query_norm = 0
    for word in query:
        if word in idf:
            query_norm += idf[word] ** 2
            for doc in inverted_index[word]:
                if doc[0] not in score_query_doc:
                    score_query_doc[doc[0]] = idf[word] * doc[1] * idf[word]
                else:
                    score_query_doc[doc[0]] += idf[word] * doc[1] * idf[word]

    query_norm = np.sqrt(query_norm)
    for doc in score_query_doc:
        score_query_doc[doc] = score_query_doc[doc] / (query_norm * doc_norms[int(doc)])

    sorted_by_second = sorted(list(score_query_doc.items()), key=lambda tup: tup[1], reverse=True)

    wine_output = []
    num = min(len(score_query_doc),10)
    for i in range(num):

        doc_id  = sorted_by_second[i][0]
        doc_score = sorted_by_second[i][1]

        title = raw_wine_data[int(doc_id)]['title']
        varietals = raw_wine_data[int(doc_id)]['variety']
        description = raw_wine_data[int(doc_id)]['description']
        profile = raw_wine_data[int(doc_id)]['profile']
        winery = raw_wine_data[int(doc_id)]['winery']
        points = raw_wine_data[int(doc_id)]['points']
        price = raw_wine_data[int(doc_id)]['price']
        region = raw_wine_data[int(doc_id)]['region_1']
        country = raw_wine_data[int(doc_id)]['country']
        province = raw_wine_data[int(doc_id)]['province']
        sommelier = raw_wine_data[int(doc_id)]['taster_name']

        wine_output.append({'sommelier':sommelier,'points':points,'price':price,'region':region,'country':country,'province':province,'winery':winery,'title':title,'varietal':varietals, 'description':description,'profile':profile})
    return wine_output



# # Wine processing
# wine_data = read_file(4)
# inverted_index_wine = read_file(12)
# #inverted_index_wine2 = build_inverted_index_wine(wine_data)
#
# num_docs_wine = len(wine_data)
# idf_dict_wine = read_file(13)
# doc_norms_wine = read_file(14)
#
# # Food Processing
# #food_data = read_csv("./data/epicurious-recipes-with-rating-and-nutrition/epi_r.csv")
# food_data = read_csv(15)
# inverted_index_food = read_file(16)
# # inverted_index_food, recipe_id_to_title = build_inverted_index_food(food_data)
# recipe_id_to_title = read_file(17)
# num_docs_food = len(food_data)
# # idf_dict_food = compute_idf(inverted_index_food, num_docs_food)
# idf_dict_food = read_file(18)
# # doc_norms_food = compute_doc_norms(inverted_index_food, idf_dict_food, num_docs_food)
# doc_norms_food = read_file(19)

class SearchType(Enum):
    FOOD = 1
    WINE = 2

# def search(query, searchType):
#   output = ""
#
#   if searchType == SearchType.WINE:
#     # wine_title, varieties, description, profile = index_search_cosine_sim_wine(query, inverted_index_wine, doc_norms_wine, idf_dict_wine, wine_data)
#     wine_output = index_search_cosine_sim_wine(query, inverted_index_wine, doc_norms_wine, idf_dict_wine, wine_data)
#     for wine in range(len(wine_output)):
#         food_words = generate_food_words(wine_output[wine]['varietal'])
#         food_words = " ".join(food_words)
#         food_output = index_search_cosine_sim_food(food_words, inverted_index_food, doc_norms_food, idf_dict_food,
#                                                    recipe_id_to_title)
#         wine_output[wine]['food'] = food_output[:3]
#
#
#
#   elif searchType == SearchType.FOOD:
#     output = index_search_cosine_sim_food(query, inverted_index_food, doc_norms_food, idf_dict_food, recipe_id_to_title)
#
#   return wine_output
  # return output, wine_title, varieties, description, profile
