from django.shortcuts import render
import os
from dotenv import load_dotenv
import requests


def base(request):
    return render(request, 'recipes/base.html')


def fetch_recipes(request):
    load_dotenv()
    tags = request.GET.get('tags', 'vegetarian,dessert')  # Default tags
    url = ("https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/"
           "recipes/random")
    querystring = {"tags": tags, "number": "1"}
    headers = {
        'X-RAPIDAPI-KEY': os.getenv('RAPIDAPI_KEY'),
        'X-RAPIDAPI-HOST': os.getenv('RAPIDAPI_HOST')
    }
    response = requests.get(url, headers=headers, params=querystring)
    recipes = response.json()
    return render(request, 'recipes/fetch_recipes.html', {'recipes': recipes})


def search_by_ingredient(request):
    load_dotenv()
    recipes = None
    if 'ingredients' in request.GET:
        ingredients = request.GET['ingredients']
        url = ("https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/"
               "recipes/findByIngredients")
        querystring = {
            "ingredients": ingredients,
            "number": "5",
            "ignorePantry": "true",
            "ranking": "1"
        }
        headers = {
            'X-RAPIDAPI-KEY': os.getenv('RAPIDAPI_KEY'),
            'X-RAPIDAPI-HOST': os.getenv('RAPIDAPI_HOST')
        }
        response = requests.get(url, headers=headers, params=querystring)
        recipes = response.json()
    return render(request,
                  'recipes/search_by_ingredient.html',
                  {'recipes': recipes})


def search_by_nutrients(request):
    load_dotenv()
    params = {
        'minProtein': request.GET.get('minProtein', 0),
        'maxCalories': request.GET.get('maxCalories', 300),
        'minCarbs': request.GET.get('minCarbs', 0),
        'maxFat': request.GET.get('maxFat', 30),
        'number': request.GET.get('number', 2)
    }
    url = ("https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/"
           "recipes/findByNutrients")
    headers = {
        'X-RAPIDAPI-KEY': os.getenv('RAPIDAPI_KEY'),
        'X-RAPIDAPI-HOST': os.getenv('RAPIDAPI_HOST')
    }
    response = requests.get(url, headers=headers, params=params)
    recipes = response.json()
    return render(request,
                  'recipes/search_by_nutrients.html',
                  {'recipes': recipes})


def recipe_details(request, recipe_id):
    load_dotenv()
    url = (f"https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/"
           f"recipes/{recipe_id}/information")
    headers = {
        'X-RAPIDAPI-KEY': os.getenv('RAPIDAPI_KEY'),
        'X-RAPIDAPI-HOST': os.getenv('RAPIDAPI_HOST')
    }
    response = requests.get(url, headers=headers)
    recipe = response.json()
    return render(request,
                  'recipes/recipe_details.html',
                  {'recipe': recipe})
