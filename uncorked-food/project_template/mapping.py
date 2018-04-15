from pandas import read_csv

mapping_chart = read_csv("./data/wine-folly-pairing-rules/wine_folly_pairings.csv")

wine_buckets = {
	'sparkling' : set(['champagne']),
	'dessert' : set(['port','sherry','botrytis','dessert','eiswein']),
	'sweet_white' : set(['moscato']),
	'light_white' : set(['riesling','pinot gris','sauvignon blanc']),
	'rich_white' : set(['chardonnay']),
	'rose' : set(['rose']),
	'bold_red' : set(['bordeaux','syrah','shiraz','malbec','mourvedre','pinotage','cabernet sauvignon','meritage']),
	'medium_red' : set(['merlot','sangiovese','zinfandel','cabernet franc','tempranillo','nebbiolo','barbera']),
	'light_red' : set(['pinot noir','gamay'])
}

food_buckets = {
	'red_meat' : set(['lamb','beef','venison']),
	'cured_meat' : set(['salami','proscuitto','bacon','ham']),
	'pork' : set(['pork','porkchop','porkloin']),
	'poultry' : set(['chicken','duck','turkey']),
	'mollusk' : set(['oyster','mussel','clam']),
	'fish' : set(['tuna','cod','trout','bass','salmon']),
	'lobster' : set(['lobster','prawn']),
	'shellfish' : set(['shellfish','crab']),
	'grilled' : set(['grilled']),
	'barbecued' : set(['barbequed']),
	'sauteed' : set(['sauteed']),
	'fried' : set(['fried']),
	'smoked' : set(['smoked']),
	'roasted' : set(['roasted']),
	'poached' : set(['poached']),
	'steamed' : set(['steamed']),
	'soft_cheese_and_cream' : set(['brie','mascarpone','mozzarella']),
	'pungent_cheese' : set(['blue cheese','gorgonzola','stilton']),
	'hard_cheese' : set(['cheddar', 'manchego', 'asiago', 'parmesan']),
	'alliums' : set(['onion','shallot','garlic','scallion']),
	'green_vegetables' : set(['broccoli','spinach','asparagus','lettuce','kale']),
	'root_vegetables' : set(['turnip','carrot']),
	'squash' : set(['butternut','pumpkin']),
	'nightshades' : set(['tomato','eggplant','bell pepper']),
	'funghi' : set(['mushroom','crimini','chanterelle','maitake']),
	'nuts' : set(['almond','peanut','pecan']),
	'seeds' : set(['sesame']),
	'beans' : set(['pinto','black bean','lentil']),
	'peas' : set(['chickpea']),
	'black_pepper' : set(['black pepper']),
	'red_pepper' : set(['chipotle', 'chili']),
 	'hot' : set(['hot sauce','sichuan']),
	'spicy' : set(['cayenne','tabasco','jalapeno','habanero']),
	'herbs' : set(['basil','oregano','thyme','tarragon']),
	'baking_spices' : set(['cinnamon','clove','allspice']),
	'exotic_spices' : set(['anise','turmeric','ginger']),
	'aromatic_spices' : set(['saffron','fennel']),
	'white_starches' : set(['flour','rice','pasta','bread','tortilla']),
	'whole_what_grains' : set(['quinoa','farro','brown rice']),
	'sweet_starchy_vegetables' : set(['sweet potato']),
	'potato' : set(['potato']),
	'fruit' : set(['pear','apple','peach','banana']),
	'berries' : set(['blackberry','strawberry','blueberry']),
 	'vanilla' : set(['vanilla','creme brulee']),
 	'caramel' : set(['caramel']),
 	'chocolate' : set(['chocolate','cacao']),
 	'coffee' : set(['coffee'])
}

def similarity(set1, set2):
	return float(len(set.intersection(set1,set2)))/len(set.union(set1,set2))

def get_wine_bucket(wine_words):
    scores = [(wine,similarity(words,wine_words)) for wine,words in wine_buckets.items()]
    scores.sort(key=lambda x: x[1], reverse=True) 
    return scores[0][0]

def wine_to_food(wine):
    food_vec = mapping_chart[wine]
    food_indices = food_vec[food_vec==2]
    food_indices = food_indices.nonzero()[0]
    food_buckets = mapping_chart['food_types'][food_indices]
    return food_buckets

def generate_food_words(wine_words):
	''' Input: list of strings
	Output: list of strings 
	Function returns the relevant food description words 
	for a given set of wine description words. '''
    wine_type = get_wine_bucket(wine_words)
    food_types = wine_to_food(wine_type)
    food_words = []
    for food in food_types:
        food_words.extend(food_buckets[food])
    return food_words

def generate_wine_words(food_words):
	''' Input: list of strings
		Output: list of strings
		Function returns the relevant wine description words 
		for an input set of food description words. '''	
	wine_words = []
	return wine_words