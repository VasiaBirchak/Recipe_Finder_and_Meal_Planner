
import http
import json
from django.http import JsonResponse
from django.shortcuts import render


def base(request):
    return render(request, 'base.html')

def fetch_recipes(request):
    conn = http.client.HTTPSConnection("spoonacular-recipe-food-nutrition-v1.p.rapidapi.com")

    headers = {
        'x-rapidapi-key': "b2b64f3bdamsh7207945d8a6e264p106fbfjsnb62b75f24e77",
        'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
    }

    conn.request("GET", "/recipes/findByIngredients?ingredients=apples%2Cflour%2Csugar&number=5&ignorePantry=true&ranking=1", headers=headers)

    res = conn.getresponse()
    data = res.read()

    recipes = json.loads(data.decode("utf-8"))
    
    return JsonResponse(recipes, safe=False)


def search_by_ingredient(request):
    recipes = None
    if 'ingredients' in request.GET:
        ingredients = request.GET['ingredients']
        conn = http.client.HTTPSConnection("spoonacular-recipe-food-nutrition-v1.p.rapidapi.com")
        
        headers = {
            'x-rapidapi-key': "b2b64f3bdamsh7207945d8a6e264p106fbfjsnb62b75f24e77",
            'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
        }
        
        conn.request("GET", f"/recipes/findByIngredients?ingredients={ingredients}&number=5&ignorePantry=true&ranking=1", headers=headers)
        
        res = conn.getresponse()
        data = res.read()
        recipes = json.loads(data.decode("utf-8"))
    return render(request, 'search_by_ingredient.html', {'recipes': recipes})


def search_by_nutrients(request):
    conn = http.client.HTTPSConnection("spoonacular-recipe-food-nutrition-v1.p.rapidapi.com")

    headers = {
        'x-rapidapi-key': "b2b64f3bdamsh7207945d8a6e264p106fbfjsnb62b75f24e77",
        'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
    }

    conn.request("GET", "/recipes/findByNutrients?minProtein=0&minVitaminC=0&minSelenium=0&maxFluoride=50&maxVitaminB5=50&maxVitaminB3=50&maxIodine=50&minCarbs=0&maxCalories=250&minAlcohol=0&maxCopper=50&maxCholine=50&maxVitaminB6=50&minIron=0&maxManganese=50&minSodium=0&minSugar=0&maxFat=20&minCholine=0&maxVitaminC=50&maxVitaminB2=50&minVitaminB12=0&maxFolicAcid=50&minZinc=0&offset=0&maxProtein=100&minCalories=0&minCaffeine=0&minVitaminD=0&maxVitaminE=50&minVitaminB2=0&minFiber=0&minFolate=0&minManganese=0&maxPotassium=50&maxSugar=50&maxCaffeine=50&maxCholesterol=50&maxSaturatedFat=50&minVitaminB3=0&maxFiber=50&maxPhosphorus=50&minPotassium=0&maxSelenium=50&maxCarbs=100&minCalcium=0&minCholesterol=0&minFluoride=0&maxVitaminD=50&maxVitaminB12=50&minIodine=0&maxZinc=50&minSaturatedFat=0&minVitaminB1=0&maxFolate=50&minFolicAcid=0&maxMagnesium=50&minVitaminK=0&maxSodium=50&maxAlcohol=50&maxCalcium=50&maxVitaminA=50&maxVitaminK=50&minVitaminB5=0&maxIron=50&minCopper=0&maxVitaminB1=50&number=10&minVitaminA=0&minPhosphorus=0&minVitaminB6=0&minFat=5&minVitaminE=0", headers=headers)

    res = conn.getresponse()
    data = res.read()

    recipes = json.loads(data.decode("utf-8"))
    
    return JsonResponse(recipes, safe=False)
