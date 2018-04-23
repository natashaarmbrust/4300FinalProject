from django.conf.urls import url

from . import views

app_name = 'pt'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'wine/?$', views.search_wine, name='search-wine'),
    url(r'food/?$', views.search_food, name='search-food'),
    url(r'search/2?$', views.result_wine, name='result-wine'),
    url(r'search/3?$', views.result_food, name='result-food'),
    ]

