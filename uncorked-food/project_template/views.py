from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from .models import Docs
from django.template import loader
from .form import QueryForm
from .test import find_similar_levenshtein, index_search_cosine_sim
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def index(request):
    output_list = ''
    output=''
    wine=''
    if request.GET.get('wine'):
        wine = request.GET.get('wine')
        output_list = index_search_cosine_sim(wine)
        # output_list = ["what's up"]
        # paginator = Paginator(output_list, 10)
        # page = request.GET.get('page')
        # try:
        #     output = paginator.page(page)
        # except PageNotAnInteger:
        #     output = paginator.page(1)
        # except EmptyPage:
        #     output = paginator.page(paginator.num_pages)
    print(output_list)
    return render_to_response('project_template/index.html',
                          {'output': output_list,
                           'input': wine,
                           'magic_url': request.get_full_path(),
                           })