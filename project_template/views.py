from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from .models import Docs
from django.template import loader
from .form import QueryForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .cosine import SearchType
# from .cosine import search
from .cosine import index_search_cosine_sim_wine, index_search_cosine_sim_food
from .utility import read_file, read_csv, tokenize
from enum import Enum
from .mapping import generate_food_words, generate_wine_words



# STATES 

START = 1
SEARCH_WINE = 2
SEARCH_FOOD = 3
RESULT_WINE = 4
RESULT_FOOD = 5

state = START

placeholder_wine = "fruity, oak, Riesling, Pinot Noir, 2017 vintage, ..."
placeholder_food = "salmon, lemon, pepper, almond, spicy, ..."
search_description_food = "Describe your food ..."
search_description_wine = "Describe your wine ..."

#SVD data
#need to save this
# food_words_compressed = read_file()
# food_word_to_index = read_file()
# food_index_to_word = read_file()


#wine_words_compressed = read_file()
#wine_word_to_index = read_file()
#wine_index_to_word = read_file()


# Wine Data
#wine_data = read_file(4)

#inverted_index_wine = read_file(12)
inverted_index_wine = read_file(23)

# idf_dict_wine = read_file(13)
idf_dict_wine = read_file(24)
# doc_norms_wine = read_file(14)
doc_norms_wine = read_file(25)
wine_data = read_file(22)
num_docs_wine = len(wine_data)

# Food Data
# food_data = read_csv(15)
food_data = read_file(5)

# inverted_index_food = read_file(16)
inverted_index_food = read_file(29)

# recipe_id_to_title = read_file(17)
num_docs_food = len(food_data)
# idf_dict_food = read_file(18)
idf_dict_food = read_file(30)

# doc_norms_food = read_file(19)
doc_norms_food = read_file(31)

# Create your views here.
def index(request):
    return render_to_response('project_template/index.html',
                              {
                              # put outputs here'
                              "state": state,
                              })

def search_wine(request):  
  state = SEARCH_WINE
  return render_to_response('project_template/index.html',
                              {
                              "state": state,
                              "search_description": search_description_food,
                              "placeholder": placeholder_food,
                              })

  

def search_food(request):
  state = SEARCH_FOOD
  return render_to_response('project_template/index.html',
                              {
                              "state": state,
                              "search_description": search_description_wine,
                              "placeholder": placeholder_wine,
                              })

# TODO: call backend method with search type to get top 3 wines based on query
 
def result_wine(request): 
  query = request.GET.get('q')
  state = RESULT_FOOD
  # Replace with actual outputs

  top10foods = index_search_cosine_sim_food(query,inverted_index_food,doc_norms_food,idf_dict_food,food_data)
  top3foods = []
  seenFoods = set()
  for food in top10foods:
      if food['title'] not in seenFoods:
          top3foods.append(food)
          seenFoods.add(food["title"])


  wine_output, buckets = from_food_get_wine(top3foods)

  results = [] 
  for i,wine in enumerate(wine_output):
    words = wine["profile"]
    result = {
      "bucket" : buckets[i][0],
      "words" : ", ".join(list(words)[:10]), # NOTE - words should be a string spereated by commas (and also we should probably reduce it to like 10 elements)
      "recipes" : [top3foods[i]]
    }

    results.append(result)

  best_choice = None
  second_choice = None
  third_choice = None

  for i, out in enumerate(wine_output):
      output = {"food": results[i], "wine": wine_output[i]}
      if i == 0:
          best_choice = output
      if i == 1:
          second_choice = output
      if i == 2:
          third_choice = output
      if i > 2:
          break

  return render_to_response('project_template/index.html',
                              {
                              "state": state,
                              "best_choice": best_choice,
                              "second_choice": second_choice,
                              "third_choice": third_choice,
                              })


def result_food(request):
  state = RESULT_WINE
  # TODO: call backend method with search type to get top 3 foods based on query
  query = request.GET.get('q')
  query=expand_query(tokenize(query), wine_words_compressed, wine_word_to_index, wine_index_to_word)

  # Replace with actual outputs
  buckets = []
  recipes = []

  # if query:
  top_3_wines = index_search_cosine_sim_wine(query,inverted_index_wine,doc_norms_wine,idf_dict_wine,wine_data)

  # TODO: call backend method with search type to get top 3 foods based on query
  food_output = from_wine_get_food(top_3_wines)

  # 
  # MARK - KEEP THIS FORMAT FOR FRONTEND 
  #

  best_choice = None
  second_choice = None
  third_choice = None

  for i,out in enumerate(food_output):
    output = {"food": food_output[i], "wine": top_3_wines[i]}
    if i == 0:
      best_choice = output
    if i == 1:
      second_choice = output
    if i == 2:
      third_choice = output
    if i > 2:
      break

  return render_to_response('project_template/index.html',
                              {
                              # put outputs here
                              "state": state,
                              "best_choice": best_choice,
                              "second_choice": second_choice,
                              "third_choice": third_choice,
                              })




"""
top3foods = [{
  rating, calories, title, ingredients, directions, categories
},...]

output = [{},...] result from cosine_sim

"""
def from_food_get_wine(top_3_foods):
  
  wine_output = []
  buckets = []
  
  for recipe in top_3_foods:
    # ingredients = recipe['ingredients']
    flavors, bucket = generate_wine_words(recipe['categories'],recipe['title'])
    flavors = " ".join(flavors)
    top_wines = index_search_cosine_sim_wine(flavors,inverted_index_wine,doc_norms_wine,idf_dict_wine,wine_data)

    buckets.append(bucket)
    wine_output.append(top_wines[0])

  return wine_output, buckets



"""
from_wine_get_food function

INPUT
====================
query: [list of dictionaries] top 3 wines output based on query from user 
  (ex: "fruity pinot oak")
  
  
[{'title': 'Bloomer Creek 2008 Riesling (Finger Lakes)', 
  'varietal': 'Riesling', 
  'description': "There's a delicate whiff of dried orange peel and apple cider vinegar on the nose of this unique Finger Lakes Riesling, but the palate is chock full of fresh apples accented by a sweet tangerine acidity and hints of clove and spice.", 
  'profile': ['dried', 'palate', 'chock', 'hints', 'vinegar', 'unique', 'full', 'fresh', 'tangerine', 'clove', 'apples', 'orange', 'apple', 'lakes', 'whiff', 'spice', 'accented', 'peel', 'cider', 'finger', 'sweet']
  }, 
 {'title': 'Lakewood 2007 Dry Riesling (Finger Lakes)', 
  'varietal': 'Riesling', 
  'description': 'Those who buy Riesling for its intense aromas will be disappointed with the subdued nose on this example from the Finger Lakes. Nonetheless, the palate delivers attractive stone fruit flavors of peach and apricot and the truly crisp, dry finish makes for a refreshing package.', 
  'profile': ['palate', 'crisp', 'package', 'peach', 'dry', 'subdued', 'aromas', 'example', 'intense', 'buy', 'stone', 'fruit', 'delivers', 'flavors', 'nose', 'finish', 'attractive', 'finger', 'apricot']
  }, 
 {'title': 'Fox Run 2007 Riesling (Finger Lakes)', 
  'varietal': 'Riesling', 
  'description': "This lively Riesling offers aromas of citrus, apricot and honey, followed by layers of white fruit, spice and pepper. The wine has a slightly sweet fruity character but it's balanced by acid and minerals. A fun but impressive Riesling.", 
  'profile': ['layers', 'minerals', 'aromas', 'character', 'offers', 'fruity', 'citrus', 'fruit', 'honey', 'white', 'spice', 'pepper', 'acid', 'impressive', 'sweet', 'fun', 'apricot']
  }]

OUTPUT
====================

food_output: [List of dictionaries] (we can also do classes too)]
  [
    {
      "bucket" : String (ex. "bold_red", "medium_red", "rose" -- Baiscally lowercase and connected with underscores)
      "words" : List of Strings (ex. ["black pepper", "hard cheese", ...])
      "recipes" : List of Dictionaries 
        [ 
          {
            "title": String,
            "rating": Float, 
            "calories": Float,
          }
        ]
        (ex. [ {title: "Lentil, Apple, and Turkey Wrap", rating: 2.5, calories; 426.0}, ...])
    }
  ]

"""
def from_wine_get_food(top_3_wines):
 
  food_output = []

  for wine in top_3_wines:
    bucket, good_words, bad_words, foods = generate_food_words(wine['varietal'], wine['profile'])
    foods = " ".join(foods)
    recipes = index_search_cosine_sim_food(foods, inverted_index_food, doc_norms_food, idf_dict_food,
                                                   food_data)
    top_recipes = []
    for recipe in recipes:
      if recipe not in top_recipes:
        top_recipes.append(recipe)
    
    result = {
      "bucket" : bucket,
      "words" : ", ".join(list(good_words)[:10]), # NOTE - words should be a string spereated by commas (and also we should probably reduce it to like 10 elements),

      "recipes" : top_recipes[:3]
    }

    food_output.append(result)

  return food_output
