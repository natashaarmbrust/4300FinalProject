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
import nltk
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
from nltk.corpus import stopwords


from .utility import read_file,read_csv,tokenize
from .wine_processing import build_inverted_index_wine
from .food_processing import build_inverted_index_food
from .mapping import generate_food_words

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

def index_search_cosine_sim_food(query, inverted_index, doc_norms, idf, index_to_title):
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

def wine_profile(descriptions):

    stop_words=set(stopwords.words('english'))
    remove_tags={"CD" , "RB", "VBZ", "VBD", "IN", "MD", "VBG", "VBP"}
    prof=set(tokenize((descriptions)))
    prof= prof - stop_words
    tagged= nltk.pos_tag(prof)

    return [x[0] for x in tagged if x[1] not in remove_tags]

def index_search_cosine_sim_wine(query, inverted_index, doc_norms, idf, index_to_title,index_to_variety):
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
    #print(sorted_by_second)
    final = []
    varieties = []
    for i in range(10):
        doc_id  = sorted_by_second[i][0]
        doc_score = sorted_by_second[i][1]
        final.append((doc_score,index_to_title[int(doc_id)],index_to_variety[int(doc_id)]))
        varieties.append(index_to_variety[int(doc_id)])
    
    #final = [(v, index_to_title[int(k)], index_to_description[int(k)]) for k, v in sorted_by_second]
    return final[:10], varieties
    #profile([x[2] for x in final[:10]])


# Wine processing

wine_data = read_file(4)
"""inverted_index_wine, docid_to_wine_title,docid_to_winedesc = build_inverted_index_wine(wine_data)
idf_dict_wine = compute_idf(inverted_index_wine, num_docs_wine)
doc_norms_wine = compute_doc_norms(inverted_index_wine, idf_dict_wine, num_docs_wine)"""

num_docs_wine = len(wine_data)



# Food Processing
food_data = read_csv("./data/epicurious-recipes-with-rating-and-nutrition/epi_r.csv")
"""inverted_index_food, recipe_id_to_title = build_inverted_index_food(food_data)
num_docs_food = len(food_data)
idf_dict_food = compute_idf(inverted_index_food, num_docs_food)
doc_norms_food = compute_doc_norms(inverted_index_food, idf_dict_food, num_docs_food)"""

num_docs_food = len(food_data)
inverted_index_food = None
recipe_id_to_title = None
idf_dict_food = None
doc_norms_food = None
docid_to_winedesc = None

def computeData(inverted_index_f, inverted_index_w):
    num_docs_food = len(food_data)
    idf_dict_food = compute_idf(inverted_index_f, num_docs_food)
    doc_norms_food = compute_doc_norms(inverted_index_f, idf_dict_food, num_docs_food)
    
    num_docs_wine = len(wine_data)
    idf_dict_wine = compute_idf(inverted_index_w, num_docs_wine)
    doc_norms_wine = compute_doc_norms(inverted_index_w, idf_dict_wine, num_docs_wine)

def saveData():
    inverted_index_food, recipe_id_to_title = build_inverted_index_food(food_data)
    num_docs_food = len(food_data)
    idf_dict_food = compute_idf(inverted_index_food, num_docs_food)
    doc_norms_food = compute_doc_norms(inverted_index_food, idf_dict_food, num_docs_food)
    
    inverted_index_wine, docid_to_wine_title,docid_to_winedesc = build_inverted_index_wine(wine_data)
    num_docs_wine = len(wine_data)
    idf_dict_wine = compute_idf(inverted_index_wine, num_docs_wine)
    doc_norms_wine = compute_doc_norms(inverted_index_wine, idf_dict_wine, num_docs_wine)

    """with open('data/jsons/food_inverted_index.json', 'w') as f:
                    json.dump(inverted_index_food, f)
            
                with open('data/jsons/recipe_id_to_title.json','w') as f:
                    json.dump(recipe_id_to_title, f)
            
                with open('data/jsons/doc_norms_food.json', 'w') as f:
                    json.dump(num_docs_food, f)
            
                with open('data/jsons/idf_dict_food.json', 'w') as f:
                    json.dump(idf_dict_food, f)
            
                with open('data/jsons/wine_inverted_index.json', 'w') as f:
                    json.dump(inverted_index_wine, f)"""

    np.savetxt("data/jsons/doc_norms_wine.txt", doc_norms_wine)

    with open('data/jsons/idf_dict_wine.json', 'w') as f:
        json.dump(idf_dict_wine, f)

    with open('data/jsons/docid_to_wine_title.json', 'w') as f:
        json.dump(docid_to_wine_title, f)

    with open('data/jsons/docid_to_winedesc.json','w') as f:
        json.dump(docid_to_winedesc, f)

def loadData():
    inverted_index_wine = None
    docid_to_wine_title = None
    docid_to_winedes = None
    idf_dict_wine = None
    doc_norms_wine = None

    with open('data/jsons/food_inverted_index.json') as f:
        inverted_index_food = json.load(f)

    with open('data/jsons/doc_norms_food.json') as f:
        doc_norms_food = json.load(f)

    with open('data/jsons/idf_dict_food.json') as f:
        idf_dict_food = json.load(f)

    with open('data/jsons/wine_inverted_index.json') as f:
        inverted_index_wine = json.load(f)

    doc_norms_wine = np.loadtxt("data/jsons/doc_norms_wine.txt")

    with open('data/jsons/idf_dict_wine.json') as f:
        idf_dict_wine = json.load(f)

    with open('data/jsons/docid_to_wine_title.json') as f:
        docid_to_wine_title = json.load(f) 

    with open('data/jsons/docid_to_winedesc.json') as f:
        docid_to_winedesc = json.load(f) 

    return inverted_index_wine,inverted_index_food, docid_to_wine_title,docid_to_winedesc, idf_dict_wine, doc_norms_wine


#saveData()

class SearchType(Enum):
    FOOD = 1
    WINE = 2 

def search(query, searchType):
  output = ""
  inverted_index_wine,inverted_index_food, docid_to_wine_title, docid_to_winedes, idf_dict_wine, doc_norms_wine = loadData()

  if searchType == SearchType.WINE:
    wine_output, varieties = index_search_cosine_sim_wine(query, inverted_index_wine, doc_norms_wine, idf_dict_wine, docid_to_wine_title,docid_to_variety)
    food_words = generate_food_words(varieties)
    food_words = " ".join(food_words)
    food_output = index_search_cosine_sim_food(food_words, inverted_index_food, doc_norms_food, idf_dict_food, recipe_id_to_title)
    output = food_output

  elif searchType == SearchType.FOOD:
    print(inverted_index_food)
    output = index_search_cosine_sim_food(query, inverted_index_food, doc_norms_food, idf_dict_food, recipe_id_to_title)
  
  return output

