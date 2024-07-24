import requests
import os
from dotenv import load_dotenv


def get_spoonacular_hash(user):
    load_dotenv()
    url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/users/connect"
    payload = {
        "username": user.username,
        "firstName": user.first_name,
        "lastName": user.last_name,
        "email": user.email
    }
    headers = {
        "X-RAPIDAPI-KEY": os.getenv('RAPIDAPI_KEY'),
        "X-RAPIDAPI-HOST":  os.getenv('RAPIDAPI_HOST'),
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data.get('hash'), data.get('spoonacularPassword'), data.get('username')
    else:
        return None, None, None
