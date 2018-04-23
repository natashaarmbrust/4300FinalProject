from .models import Docs
import os
import Levenshtein
import json
import re
import numpy as np
from collections import defaultdict
from collections import Counter
import math
from .utility import *



def build_inverted_index_wine(msgs):
	inverted_index = dict()
	doc_idx = 0
	docid_to_winetitle = dict()
	docid_to_winedesc = dict()
	docid_to_variety = dict()
	for wine in msgs:
		s = ' '
		string_list = [wine['title'],wine['variety'],wine['region_1'],wine['province'],wine['country'],wine['winery'],wine['description']]
		wine_tokens = tokenize(s.join(filter(None, string_list)))
		for word in wine_tokens:
			if word not in inverted_index:
				inverted_index[word] = dict()
				inverted_index[word][str(doc_idx)] = 1
			elif str(doc_idx) not in inverted_index[word]:
				inverted_index[word][str(doc_idx)] = 1
			else:
				inverted_index[word][str(doc_idx)] += 1
		docid_to_winetitle[doc_idx] = wine['title']
		docid_to_winedesc[doc_idx] = wine['description'] # Unused currently
		docid_to_variety[doc_idx] = wine['variety']
		doc_idx += 1

	for word in inverted_index:
		inverted_index[word] = list(inverted_index[word].items())
	return inverted_index, docid_to_winetitle, docid_to_variety









