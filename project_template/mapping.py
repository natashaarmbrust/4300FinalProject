import numpy as np
# from pandas import read_csv
from .utility import read_csv



''' VARIABLES AND FUNCTIONS FOR BOTH DIRECTIONS '''

# mapping_chart = read_csv("../data/wine-folly-pairing-rules/wine_folly_pairings.csv")
mapping_chart = read_csv(20)

wine_buckets = {
	'sparkling' : set(['champagne','prosecco','sparkling blend']),
	'dessert' : set(['port','sherry','muscat','dessert','eiswein','madeira']),
	'sweet_white' : set(['moscato','riesling','chenin blanc','gewurztraminer','muscadelle','white blend']),
	'light_white' : set(['pinot blanc','pinot gris','sauvignon blanc','pinot grigio','trebbiano','sylvaner']),
	'rich_white' : set(['chardonnay','semillon','viognier','marsanne','roussanne','bordeaux-style white blend']),
	'rose' : set(['rose','white zinfandel']),
	'bold_red' : set(['bordeaux-style red blend','syrah','shiraz','malbec','mourvedre','pinotage','cabernet sauvignon','meritage','bordeaux','cabernet']),
	'medium_red' : set(['merlot','sangiovese','zinfandel','cabernet franc','tempranillo','nebbiolo','barbera','tinta de toro','red blend']),
	'light_red' : set(['pinot noir','gamay','grenache','carignan','counoise'])
}

food_buckets = {
	'red_meat' : set(['lamb','beef','venison', 'veal', 'mutton', 'ground beef', 'bison', 'steak', 'ground lamb']),
	'cured_meat' : set(['salami','proscuitto','bacon','ham', 'bologna', 'chorizo', 'guanciale','liverworst', 'pancetta','pepperoni', 'sausage', 'capicollo', 'copa']),
	'pork' : set(['pork','porkchop','porkloin', 'tenderloin' 'pork shoulder','pork belly','crackling', 'ground pork']),
	'poultry' : set(['chicken','duck','turkey', 'qual', 'goose']),
	'mollusk' : set(['oyster','mussel','clam', 'scallop','geoduck', 'octopus', 'squid']),
	'fish' : set(['tuna','cod','trout','bass','salmon', 'anchovy','bream','catfish','cod','eel','flounder','grouper','haddock','halibut','herring','mackerel', 'mahi mahi','monkfish','mullet','pike','pollock','snapper','sole','tilapia','tuna','whitefish']),
	'lobster' : set(['lobster','prawn']),
	'shellfish' : set(['shellfish','crab','crayfish','shrimp']),
	'grilled' : set(['grilled', 'rotisserie', 'broil','char']),
	'barbecued' : set(['barbequed']),
	'sauteed' : set(['sauteed']),
	'fried' : set(['fried']),
	'smoked' : set(['smoked']),
	'roasted' : set(['roasted', 'toast', 'bake','sear']),
	'poached' : set(['poached', 'coddle']),
	'steamed' : set(['steamed','steam']),
	'soft_cheese_and_cream' : set(['brie','mascarpone','mozzarella','camembert','feta','ricota','cream','milk','anejo','boursin','burrata','chevre','cottage cheese']),
	'pungent_cheese' : set(['blue cheese','gorgonzola','stilton']),
	'hard_cheese' : set(['cheddar', 'manchego', 'asiago', 'parmesan','comte','gouda','manchego','pecornino']),
	'alliums' : set(['onion','shallot','garlic','scallion','chive','leek','scape','']),
	'green_vegetables' : set(['broccoli','spinach','asparagus','lettuce','kale','cabbage','collard greens','lettuce','chard','brussels sprot','pea','cucumber','asparagus','green bean','artichoke','zuchini','okra']),
	'root_vegetables' : set(['turnip','carrot','beet','parsnip','potato','sweet potato','lotus root','yams','sunchoke','rutabaga','daikon','yucca']),
	'squash' : set(['butternut','pumpkin','gourd','acorn squash','kabocha','spaghetti squash','red kuri','delicata',]),
	'nightshades' : set(['tomato','eggplant','bell pepper']),
	'funghi' : set(['mushroom','crimini','chanterelle','maitake','morel','enoki','shiitake','portobello','oyster','button','porcini']),
	'nuts' : set(['almond','peanut','pecan','walnut','cashew','pistachio','hazlenut','macadamia','brazil nut']),
	'seeds' : set(['sesame','chia','flax','hemp','poppy','sunflower seeds']),
	'beans' : set(['pinto','black bean','lentil','navy','kidney','black-eyed','cannellini','great northern','lima','fava','lentils']),
	'peas' : set(['chickpea','peas']),
	'black_pepper' : set(['black pepper']),
	'red_pepper' : set(['chipotle', 'chili', 'red pepper']),
	'spicy' : set(['cayenne','tabasco','jalapeno','habanero','hot sauce','sichuan','siracha','tabasco','thai pepper','thai chile','serrano','hatch','poblano','ancho chile','shishito','pimento','harissa','chili oil','pico de gallo']),
	'herbs' : set(['basil','oregano','thyme','tarragon','rosmary','parsley','dill','sage','marjoram','coriander','lemongrass','chives',]),
	'baking_spices' : set(['cinnamon','clove','allspice','nutmeg','anise','cocoa','cardamom','cassia']),
	'exotic_spices' : set(['anise','turmeric','ginger','grains of paradise', 'sumac', 'cumin','curry powder','fenugreek','sumac','five spice','garam masala']),
	'aromatic_spices' : set(['saffron','fennel']),
	'white_starches' : set(['flour','rice','pasta','bread','tortilla']),
	'whole_what_grains' : set(['quinoa','farro','brown rice']),
	'potato' : set(['potato', 'sweet potato',]),
	'fruit' : set(['pear','apple','peach','banana','mango','cantaloupe','clementine','orange','tangerine','fig','grapefruit','grape','kiwi','plum','lemon','lime','papaya','peach','pineapple','watermelon']),
	'berries' : set(['blackberry','strawberry','blueberry','raspberry','cherry','pomegranate','cranberry','']),
 	'vanilla' : set(['vanilla','creme brulee','cream']),
 	'caramel' : set(['caramel','nougat','toffee','salted caramel']),
 	'chocolate' : set(['chocolate','cacao','hot chocolate','milk chocolate','dark chocolate', 'white chocolate']),
 	'coffee' : set(['coffee', 'espresso', 'cappuccino','mocha','coffee liqueur'])
}

wine_good_bad = {
	'sweet' : ( set(['spicy','hot','spice','sweet','spice','salt']), set(['fat','butter','cream','rich']) ),
	'acidic' : ( set(['butter','fatty','salt','creamy','heavy']), set(['chocolate','coffee']) ),
	'rich' : ( set(['butter','cream','hearty','savory']), set(['acidic','sour','light']) ),
	'tannin' : ( set(['fat','rich','meat','heavy','succulent']), set(['spicy','bitter','chocolate','fish']) )
}

taste_descriptors = {
	'sweet' : set(['fruity','honey','vanilla','dessert','cake','sugar','syrup']),
	'fruity' : set(['sweet','jam','candied','sweetened','nectar','berry','fruit']),
	'sour' : set(['acid','acidity','acidic','briny','brine','tangy','lime']),
	'acidic' : set(['sour','tart','snappy','citrus','vinegar','fermented','lemon']),
	'rich' : set(['creamy','full body','full','rich','fatty','buttery','butter','cream','oily','milky']), 
	'tannin' : set(['smoke','meat','spice','dry','bold','tannin','tannic','astringent','rough','bitter','harsh'])
}

def similarity(set1, set2):
	return float(len(set.intersection(set1,set2)))/len(set.union(set1,set2))



''' FUNCTIONS FOR WINE -> FOOD '''

def get_wine_bucket(wine_words):
    scores = [(wine,similarity(words,wine_words)) for wine,words in wine_buckets.items()]
    scores.sort(key=lambda x: x[1], reverse=True) 
    # print(similarity(set([wine_words]),wine_buckets['light_white']))
    # print(similarity(wine_buckets['light_white'],set([wine_words])))
    # print(scores)
    # print(wine_words)
    return scores[0][0]
    # threshold = .0001
    # buckets = []
    # for i in range(3):
    # 	if scores[i][1] > threshold:
    # 		buckets.append(scores[i][0])
    # return buckets

def wine_to_food(wine):
    food_vec = mapping_chart[wine].as_matrix()
    food_indices = np.where(food_vec==2)[0]
    food_types = mapping_chart['food_types'][food_indices]
    return food_types

def filter_wine_word(word):
	### HERE INCORPORATE THESAURUS
	for descriptor, words in taste_descriptors.items():
		if word in words and descriptor in wine_good_bad.keys():
			return wine_good_bad[descriptor]
	else:
		return set([word]), set([])

def generate_food_words(varietal, wine_words):
	''' Input: list of strings
	Output: list of strings 
	Function returns the relevant food description words 
	for a given set of wine description words. '''
	
	output = []

	wine_words = set([word.lower() for word in wine_words])
	good_flavors, bad_flavors = zip(*map(filter_wine_word, wine_words))
	good_flavors = set.union(*good_flavors)
	bad_flavors = set.union(*bad_flavors)

	# varietals = set([word.lower() for word in varietals])
	print("varietal", varietal)
	wine_type = get_wine_bucket(set([varietal.lower()]))

	# for wine_type in wine_types:
	food_types = wine_to_food(wine_type)
	food_flavors = set(good_flavors)
	for food in food_types:
		food_flavors = set.union(food_flavors,food_buckets[food])
	food_words = set.difference(food_flavors,bad_flavors)

	
		# output.append(sub_output)

	# return output
	return wine_type, good_flavors, list(food_words)


''' FUNCTIONS FOR FOOD -> WINE '''

def extract_food_types(food_words):
    ### HERE INCORPORATE THESAURUS
	threshold = .2
	food_types = []
	scores = [(f_type,similarity(words,food_words)) for f_type,words in food_buckets.items()]
	scores.sort(key=lambda x: x[1], reverse=True) 
	for (f_type, score) in scores:
		if score >= threshold:
			food_types.append(f_type)
		else:
			break
	return food_types

def food_to_wine(food):
    wine_vec = mapping_chart.loc[mapping_chart['food_types']==food]
    if wine_vec.empty:
        return set()
    wine_vec = wine_vec.as_matrix()[0][1:]
    wine_indices = np.where(wine_vec==2)[0]
    wine_types = mapping_chart.keys()[wine_indices+1]
    return set(wine_types)

def generate_wine_words(food_words, fat, sodium):
	''' Input: list of strings
		Output: list of strings
		Function returns the relevant wine description words 
		for an input set of food description words. '''	

	wine_words = set()
	food_types = extract_food_types(food_words)
	for food in food_types:
		wine_types = food_to_wine(food)
		for wine in wine_types:
			wine_words = set.union(wine_words, wine_buckets[wine])        

	salt_threshold = 800

	if sodium > salt_threshold:
		wine_words = set.union(wine_words, taste_descriptors['sweet'], taste_descriptors['sour'])

	fat_threshold = 15        
	if fat > fat_threshold:
		wine_words = set.union(wine_words, taste_descriptors['tannin'], taste_descriptors['acidic'], taste_descriptors['rich'])
		wine_words = set.difference(wine_words, taste_descriptors['sweet'])

    ### HERE INCORPORATE THESAURUS
	not_rich = True
	for word in taste_descriptors['rich']:
		if word in food_words and not_rich:
			wine_words = set.union(wine_words, taste_descriptors['rich'], taste_descriptors['acidic'])
			not_rich = False

	not_sweet = True
	for word in taste_descriptors['sweet']:
		if word in food_words and not_sweet:
			wine_words = set.union(wine_words, taste_descriptors['fruity'])
			not_sweet = False

	not_sweet = True
	for word in taste_descriptors['fruity']:
		if word in food_words and not_sweet:
			wine_words = set.union(wine_words, taste_descriptors['sweet'])
			not_sweet = False

	not_sour = True
	for word in taste_descriptors['acidic']:
		if word in food_words and not_sour:
			wine_words = set.union(wine_words, taste_descriptors['sour'])
			not_sour = False

	not_sour = True
	for word in taste_descriptors['sour']:
		if word in food_words and not_sour:
			wine_words = set.union(wine_words, taste_descriptors['acidic'])
			not_sour = False

	if 'bitter' in food_words:
		wine_words = set.difference(wine_words, taste_descriptors['tannin'])

	return list(wine_words)