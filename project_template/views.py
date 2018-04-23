from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from .models import Docs
from django.template import loader
from .form import QueryForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .cosine import SearchType
from .cosine import search
from .cosine import index_search_cosine_sim_wine, index_search_cosine_sim_food
from .utility import read_file, read_csv
from enum import Enum

# STATES 

START = 1
SEARCH_WINE = 2
SEARCH_FOOD = 3
RESULT_WINE = 4
RESULT_FOOD = 5

state = START

placeholder_wine = "Input wine characteristics"
placeholder_food = "Input food characteristics"

# Wine Data
wine_data = read_file(4)
inverted_index_wine = read_file(12)
num_docs_wine = len(wine_data)
idf_dict_wine = read_file(13)
doc_norms_wine = read_file(14)

# Food Data
food_data = read_csv(15)
inverted_index_food = read_file(16)
recipe_id_to_title = read_file(17)
num_docs_food = len(food_data)
idf_dict_food = read_file(18)
doc_norms_food = read_file(19)

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
                              "placeholder": placeholder_food,
                              })

  

def search_food(request):
  state = SEARCH_FOOD
  return render_to_response('project_template/index.html',
                              {
                              "state": state,
                              "placeholder": placeholder_wine,
                              })

# TODO: call backend method with search type to get top 3 wines based on query
 
def result_wine(request): 
  query = request.GET.get('q')
  state = RESULT_FOOD
  # Replace with actual outputs

  if query:
      # TODO 
      top_wine_outputs = ['Wine 1', 'Wine2', 'Wine3']
  
  return render_to_response('project_template/index.html',
                              {
                              "state": state,
                              "top_outputs" : top_wine_outputs,
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

  return render_to_response('project_template/index.html',
                              {
                              # put outputs here
                                'top_3_wines':top_3_wines,
                              "state": state,
                              "food_output" : food_output,
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
def from_wine_get_food(query):

  # FAKE DATA - TODO: REPLACE 
  food_output = [{"bucket" : "bold_red", 
                  "words" : ["black pepper", "hard cheese"], 
                  "recipes" : [ {"title": "Lentil, Apple, and Turkey Wrap", "rating": 2.5, "calories": 426.0},
                                {"title": "Amazing recipe", "rating": 10, "calories": 800.0}]},
                {"bucket" : "medium_red", 
                  "words" : ["fungi", "something"], 
                  "recipes" : [ {"title": "Some sort of yummy recipe", "rating": 2.5, "calories": 426.0},
                                {"title": "yummy yummy yummy", "rating": 10, "calories": 800.0}]},

                {"bucket" : "dessert", 
                  "words" : ["fungi", "something"], 
                  "recipes" : [ {"title": "Some sort of yummy recipe", "rating": 2.5, "calories": 426.0},
                                {"title": "yummy yummy yummy", "rating": 10, "calories": 800.0}]}]


  return food_output
