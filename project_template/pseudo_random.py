import random

def get_index(query):
	random.seed(len(query))
	return random.randint(0, 2)

def expand_word(word):
	return word

def expand_query(query, word_list):
	idx = get_index(query)
	to_expand = word_list[idx:][::3]
	expanded = [expand_word(word) for word in to_expand]

	return word_list + expanded

print(expand_query('cabets', ['one','two','three','four','five']))