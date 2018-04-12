from .models import Docs
import os
import Levenshtein
import json
import re



def read_file(n):
	path = Docs.objects.get(id = n).address;
	file = open(path)
	transcripts = json.load(file)
	return transcripts

wine_data = read_file(4)

def _edit(query, msg):
    return Levenshtein.distance(query.lower(), msg.lower())


def tokenize(text):
	"""Returns a list of words that make up the text.

    Note: for simplicity, lowercase everything.
    Requirement: Use Regex to satisfy this function

    Params: {text: String}
    Returns: Array
    """

	tokenized_text = text.lower()
	tokenized_text = re.findall(r'[a-z]+',tokenized_text)  # splits string with delimiter being everything except alphabetical letters
	return tokenized_text


def find_similar(query):
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


