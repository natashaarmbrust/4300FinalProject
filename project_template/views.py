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
from .utility import read_file, read_csv
from enum import Enum
from .mapping import generate_food_words 

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

# Wine Data
#wine_data = read_file(4)

#inverted_index_wine = read_file(12)
inverted_index_wine = read_file(23)

# idf_dict_wine = read_file(13)
idf_dict_wine = read_file(24)
# doc_norms_wine = read_file(14)
doc_norms_wine = read_file(25)
print("files loaded")
wine_data = read_file(22)
print("files loaded?")
num_docs_wine = len(wine_data)

# Food Data
# food_data = read_csv(15)
food_data = read_file(5)

# inverted_index_food = read_file(16)
inverted_index_food = read_file(26)

recipe_id_to_title = read_file(17)
num_docs_food = len(food_data)
# idf_dict_food = read_file(18)
idf_dict_food = read_file(27)

# doc_norms_food = read_file(19)
doc_norms_food = read_file(28)

# Create your views here.
def index(request):
    print(state)
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

  top3foods = index_search_cosine_sim_food(query,inverted_index_food,doc_norms_food,idf_dict_food,food_data)

  wine_output = from_food_get_wine(top3foods)

  # top_wine_outputs = []
  # if query:
  #     # TODO
  #     top_wine_outputs = ['Wine 1', 'Wine2', 'Wine3']

  best_choice = None
  second_choice = None
  third_choice = None

  for i, out in enumerate(wine_output):
      if i == 0:
          best_choice = wine_output[i]
      if i == 1:
          second_choice = wine_output[i]
      if i == 2:
          third_choice = wine_output[i]
      if i > 2:
          break

  return render_to_response('project_template/index.html',
                              {
                              "state": state,
                                'top_3_foods':top3foods,
                                  "best_choice": best_choice,
                                  "second_choice": second_choice,
                                  "third_choice": third_choice,
                              })


def result_food(request):
  state = RESULT_WINE
  # TODO: call backend method with search type to get top 3 foods based on query
  query = request.GET.get('q')
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
"""
def from_food_get_wine(query):
  pass



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

  # FAKE DATA - TODO: REPLACE 
  food_output = [{"bucket" : "bold_red", 
                  "words" : "black pepper, hard cheese", 
                  "recipes" : [ 
                      {
                      "directions": 
                      ["Blanch peas in medium saucepan of boiling salted water 1 minute. Add carrots and blanch 1 minute longer. Drain. Rinse under cold water. Drain well.", "Cook fettuccine in large pot of boiling salted water until pasta is tender but still firm to bite.", "Meanwhile, heat oil in large nonstick skillet over high heat. Sprinkle fish with salt and pepper. Add fish to skillet and saut\u00e9 until golden brown and almost cooked through, about 2 minutes. Using slotted spoon, transfer fish to plate. Tent with foil to keep warm. Add parsley and flour to skillet; stir 30 seconds. Add clam juice, broth, wine and lemon juice. Simmer until sauce thickens, stirring constantly, about 2 minutes. Add sugar snap peas and carrots; stir 1 minute. Add fish; stir gently until heated through, about 1 minute. Season with salt and pepper.", "Drain pasta. Divide among 4 plates. Spoon fish, vegetables and sauce over. Sprinkle with green onions and paprika. Serve with lemon wedges."], 

                        "title": "Fettuccine with Swordfish and Sugar Snap Peas ", 

                        "ingredients": 
                        ["12 ounces sugar snap peas, trimmed", "2 medium carrots, peeled, cut into matchstick-size strips (about 2 cups)", "8 ounces fettuccine", "2 teaspoons olive oil", "1 pound skinless swordfish steaks, cut into 3/4-inch cubes", "3 tablespoons chopped fresh parsley", "1 tablespoon all purpose flour", "1/2 cup bottle clam juice", "1/2 cup canned low-salt chicken broth", "1/2 cup dry white wine", "1 1/2 tablespoons fresh lemon juice", "4 green onions, thinly sliced", "1/2 teaspoon paprika", "Lemon wedges"]
                      },
                    {"title": "Amazing recipe", "rating": 10, "calories": 800.0}]},
                {"bucket" : "medium_red", 
                  "words" : ["fungi", "something"], 
                  "recipes" : [ {"title": "Some sort of yummy recipe", "rating": 2.5, "calories": 426.0},
                                {"title": "yummy yummy yummy", "rating": 10, "calories": 800.0}]},

                {"bucket" : "dessert", 
                  "words" : ["fungi", "something"], 
                  "recipes" : [ {"title": "Some sort of yummy recipe", "rating": 2.5, "calories": 426.0},
                    {"title": "yummy yummy yummy", "rating": 10, "calories": 800.0}]}]
  
  food_output = []

  for wine in top_3_wines:
    bucket, words, foods = generate_food_words(wine['varietal'], wine['profile'])
    print("Bucket", bucket)
    foods = " ".join(foods)
    recipes = index_search_cosine_sim_food(foods, inverted_index_food, doc_norms_food, idf_dict_food,
                                                   food_data)
    top_recipes = []
    for recipe in recipes:
      if recipe not in top_recipes:
        top_recipes.append(recipe)
    
    result = {
      "bucket" : bucket,
      "words" : ", ".join(list(words)[:10]), # NOTE - words should be a string spereated by commas (and also we should probably reduce it to like 10 elements)
      "recipes" : top_recipes[:3]
    }

    food_output.append(result)

  return food_output
