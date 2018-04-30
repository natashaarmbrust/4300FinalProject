import numpy as np
import math
from .utility  import *

"""
builds inverted index and id to recipe title index 
[data] is a pandas DataFrame
"""
def build_inverted_index_food(data):

    food_data = data.as_matrix()
    title_to_index = {d[0]: i for i,d in enumerate(food_data)}
    index_to_title = {i: d[0] for i,d in enumerate(food_data)}

    # create set of tokens: these include binary features / recipe title names
    binary_name_to_index = {}
    tokens = set()

    # loop through binary features and add column headers to tokens list
    for i,name in enumerate(list(data)[6:]):
      token_list = tokenize(name)
      for t in token_list:
          tokens.add(t)
          if t in binary_name_to_index:
              binary_name_to_index[t].append(i)
          else:
              binary_name_to_index[t] = [i]

    binary_index_to_name = {}
    for k,v in binary_name_to_index.items():
      for i in v:
          binary_index_to_name[i] = k

    # add all words in recipe title to tokens list
    for title in food_data[:,0]:
      token_list = tokenize(title)
      for t in token_list: tokens.add(t)

    inverted_index = {t: [] for t in tokens}

    # create inverted index based on token list
    for i,row in enumerate(food_data):
      title = row[0]
      token_list = tokenize(title)

      token_set = set() # all tokens for this recipe
      for t in token_list:
          token_set.add(t)
      for index,binary in enumerate(row[6:]):
          if binary:
              t = binary_index_to_name[index]
              token_set.add(t)

      for t in token_set:
          inverted_index[t].append((i,1))

    return inverted_index, index_to_title

def build_inverted_index_food(msgs):
    inverted_index = dict()
    doc_idx = 0

    for food in msgs:
        if 'title' in food:
            s = ' '
            string_list = [food['title']] + list(food['ingredients']) + list(food['categories'])
            wine_tokens = tokenize(s.join(filter(None, string_list)))
            for word in wine_tokens:
                if word not in inverted_index:
                    inverted_index[word] = dict()
                    inverted_index[word][str(doc_idx)] = 1
                elif str(doc_idx) not in inverted_index[word]:
                    inverted_index[word][str(doc_idx)] = 1
                else:
                    inverted_index[word][str(doc_idx)] += 1

            doc_idx += 1

    for word in inverted_index:
        inverted_index[word] = list(inverted_index[word].items())
    return inverted_index