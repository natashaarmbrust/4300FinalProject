from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from .models import Docs
from django.template import loader
from .form import QueryForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .cosine import SearchType
from .cosine import search

# Create your views here.
def index(request):

    output_wine = ''
    output_food = ''
    query_food = ''
    query_wine = ''
    if request.GET.get('wine'):
        query_wine = request.GET.get('wine')
        output_wine = search(query_wine, SearchType.WINE)
    if request.GET.get('food'):
        query_food = request.GET.get('food')
        output_food = search(query_food, SearchType.FOOD)
        
        # output_list = ["what's up"]
        # paginator = Paginator(output_list, 10)
        # page = request.GET.get('page')
        # try:
        #     output = paginator.page(page)
        # except PageNotAnInteger:
        #     output = paginator.page(1)
        # except EmptyPage:
        #     output = paginator.page(paginator.num_pages)

    return render_to_response('project_template/index.html',
                          {'output_wine': output_wine,
                           'output_food': output_food,
                           'input_wine': query_wine,
                           'input_food': query_food,
                           'magic_url': request.get_full_path(),
                           })