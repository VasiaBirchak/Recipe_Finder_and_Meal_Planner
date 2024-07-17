# recipes/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('base/', views.base, name='base'),
    path('fetch-recipes/', views.fetch_recipes, name='fetch_recipes'),
    path('search_by_ingredient', views.search_by_ingredient, name='search_by_ingredient'),
    path('search_by_nutrients', views.search_by_nutrients, name='search_by_nutrients')
]
