import requests
from bs4 import BeautifulSoup

syns=set()

term=input("thesuarus term: ")
def get_synonyms(term, wordset):
	site= 'http://www.thesaurus.com/browse/'
	# hdrs ={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
	wordset.add(term)
	session= requests.Session()
	page= site+term
	result=session.get(page)
	c= result.content
	soup= BeautifulSoup(c, "html.parser")
	description=soup.find("strong", { "class" : "ttl" }).contents[0]
	wordset.update(description.split(","))
	words= soup.find("div", { "class" : "relevancy-list" })
	lists=words.findAll("li")
	for word in lists:
		wordset.add(word.find('span',{ "class" : "text" }).contents[0])

	return wordset

get_synonyms(term, syns)
print(syns)