import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client
from recipes.models import UserProfile
from unittest.mock import patch
from datetime import datetime


@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='testpass')


@pytest.fixture
def user_profile(user):
    if not UserProfile.objects.filter(user=user).exists():
        return UserProfile.objects.create(user=user,
                                          spoonacular_hash='fake_hash',
                                          spoonacular_username='testuser303')
    return UserProfile.objects.get(user=user)


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def mock_dotenv():
    with patch('recipes.views.load_dotenv') as mock_load_dotenv:
        yield mock_load_dotenv


@pytest.fixture
def mock_requests_get():
    with patch('requests.get') as mock_get:
        yield mock_get


@pytest.fixture
def mock_requests_delete():
    with patch('requests.delete') as mock_delete:
        yield mock_delete


@pytest.mark.django_db
def test_fetch_recipes(client, requests_mock):
    url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/random"
    requests_mock.get(url, json={"recipes": [{"id": 1, "title": "Test Recipe"}]})
    response = client.get(reverse('fetch_recipes'))
    assert response.status_code == 200
    assert 'Test Recipe' in response.content.decode()


@pytest.mark.django_db
def test_add_recipe_to_plan(client, user, user_profile, requests_mock):
    client.login(username='testuser', password='testpass')
    recipe_details_url = ("https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/"
                          "recipes/1/information")
    requests_mock.get(recipe_details_url, json={
        "id": 1,
        "title": "Test Recipe",
        "image": "test_image",
        "readyInMinutes": 30,
        "servings": 4
    })

    add_recipe_url = ("https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/"
                      f"mealplanner/{user_profile.spoonacular_username}/items")
    requests_mock.post(add_recipe_url, json={"status": "success"})
    response = client.post(reverse('add_recipe_to_plan'), {
        'recipe_id': 1,
        'date': '2024-07-25',
        'slot': 1,
        'position': 0
    })
    assert response.status_code == 302
    messages = list(response.wsgi_request._messages)
    assert len(messages) == 1
    assert str(messages[0]) == 'The dish has been successfully added to the plan!'


@pytest.mark.django_db
def test_view_weekly_plan(client, user, user_profile, mock_dotenv, mock_requests_get):
    client.login(username='testuser', password='testpass')
    mock_response = mock_requests_get.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "monday": [{"title": "Monday"}],
        "tuesday": [{"title": "Tuesday"}]
    }
    date = datetime.now().strftime('%Y-%m-%d')
    response = client.get(reverse('view_weekly_plan'), {'date': date})
    assert response.status_code == 200
    content = response.content.decode()
    assert 'Select a date:' in content


@pytest.mark.django_db
def test_delete_recipe_from_plan(client, user, user_profile, mock_dotenv, mock_requests_delete):
    client.login(username='testuser', password='testpass')
    item_id = 1
    mock_response = mock_requests_delete.return_value
    mock_response.status_code = 200

    response = client.post(reverse('delete_recipe_from_plan', args=[item_id]))
    assert response.status_code == 302
    messages = list(response.wsgi_request._messages)
    assert len(messages) == 1
    assert str(messages[0]) == 'The dish has been successfully removed from the plan!'
