from django.urls import path
from . import views

urlpatterns = [
    path('base/', views.base, name='base'),
    path('fetch-recipes/',
         views.fetch_recipes,
         name='fetch_recipes'),
    path('search_by_ingredient',
         views.search_by_ingredient,
         name='search_by_ingredient'),
    path('search_by_nutrients',
         views.search_by_nutrients,
         name='search_by_nutrients'),
    path('recipe/<int:recipe_id>/',
         views.recipe_details,
         name='recipe_details'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('add-recipe-to-plan/', views.add_recipe_to_plan, name='add_recipe_to_plan'),
    path('view-weekly-plan/', views.view_weekly_plan, name='view_weekly_plan')
]
