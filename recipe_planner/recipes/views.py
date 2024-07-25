from django.shortcuts import render, redirect
import os
from dotenv import load_dotenv
import requests
from django.contrib.auth import login, logout
from .forms import SignUpForm, LoginForm
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import AddRecipeToPlanForm
from .forms import DateFilterForm
from datetime import datetime
from django.contrib import messages


def base(request):
    return render(request, 'recipes/base.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')
            user.save()
            login(request, user)
            return redirect('base')
    else:
        form = SignUpForm()
    return render(request, 'recipes/signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('base')
    else:
        form = LoginForm()
    return render(request, 'recipes/login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return redirect('base')


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


@login_required
def add_recipe_to_plan(request):
    load_dotenv()
    if request.method == 'POST':
        form = AddRecipeToPlanForm(request.POST)
        if form.is_valid():
            user_profile = UserProfile.objects.get(user=request.user)
            spoonacular_hash = user_profile.spoonacular_hash
            recipe_id = form.cleaned_data['recipe_id']
            # Get recipe details
            details_url = ("https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/"
                           f"recipes/{recipe_id}/information")
            headers = {
                "x-rapidapi-key": os.getenv('RAPIDAPI_KEY'),
                "x-rapidapi-host":  os.getenv('RAPIDAPI_HOST')
            }
            response = requests.get(details_url, headers=headers)
            if response.status_code != 200:
                return render(request, 'recipes/add_recipe_to_plan.html',
                              {'form': form,
                               'error': 'Unable to retrieve recipe details. Try again.'})
            recipe_details = response.json()
            payload = {
                "date": int(form.cleaned_data['date'].strftime('%s')),
                "slot": form.cleaned_data['slot'],
                "position": form.cleaned_data['position'],
                "type": "RECIPE",
                "value": {
                    "id": recipe_id,
                    "title": recipe_details.get('title'),
                    "image": recipe_details.get('image'),
                    "readyInMinutes": recipe_details.get('readyInMinutes'),
                    "servings": recipe_details.get('servings'),
                }
            }
            post_url = ("https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/"
                        f"mealplanner/{user_profile.spoonacular_username}/items")
            querystring = {"hash": spoonacular_hash}
            post_response = requests.post(post_url,
                                          json=payload,
                                          headers=headers,
                                          params=querystring)
            if post_response.status_code == 200:
                messages.success(request, 'The dish has been successfully added to the plan!')
                return redirect('add_recipe_to_plan')
            else:
                return render(request, 'recipes/add_recipe_to_plan.html',
                              {'form': form,
                               'error': 'Failed to add dish to meal plan. Try again.'})
    else:
        form = AddRecipeToPlanForm()
    return render(request, 'recipes/add_recipe_to_plan.html', {'form': form})


@login_required
def view_weekly_plan(request):
    load_dotenv()
    user_profile = UserProfile.objects.get(user=request.user)
    spoonacular_hash = user_profile.spoonacular_hash
    form = DateFilterForm(request.GET or None)
    date = form.cleaned_data.get('date') if form.is_valid() else None
    if not date:
        date = datetime.now().strftime('%Y-%m-%d')
    else:
        date = date.strftime('%Y-%m-%d')
    url = ("https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/"
           f"mealplanner/{user_profile.spoonacular_username}/week/{date}")
    headers = {
        "X-RAPIDAPI-KEY": os.getenv('RAPIDAPI_KEY'),
        "X-RAPIDAPI-HOST": os.getenv('RAPIDAPI_HOST')
    }
    querystring = {"hash": spoonacular_hash}
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        weekly_plan = response.json()
        return render(request, 'recipes/view_weekly_plan.html',
                      {'weekly_plan': {date: weekly_plan}, 'form': form})
    else:
        return render(request, 'recipes/view_weekly_plan.html',
                      {'error': 'Failed to get meal plan. Try again.'})


@login_required
def delete_recipe_from_plan(request, item_id):
    load_dotenv()
    user_profile = UserProfile.objects.get(user=request.user)
    spoonacular_hash = user_profile.spoonacular_hash
    url = ("https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/"
           f"mealplanner/{user_profile.spoonacular_username}/items/{item_id}")
    querystring = {"hash": spoonacular_hash}
    headers = {
        "x-rapidapi-key": os.getenv('RAPIDAPI_KEY'),
        "x-rapidapi-host": os.getenv('RAPIDAPI_HOST'),
        "Content-Type": "application/json"
    }
    response = requests.delete(url, headers=headers, params=querystring)
    if response.status_code == 200:
        messages.success(request, 'The dish has been successfully removed from the plan!')
    else:
        messages.error(request, 'Failed to remove dish from meal plan. Try again.')
    return redirect('view_weekly_plan')
