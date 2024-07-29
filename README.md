# Recipe Finder and Meal Planner

## Functionality of the Recipe Finder and Meal Planner Application

This web app allows users to find recipes based on the ingredients they have and plan their meals for the week. Here are the main features of the app:

### 1. Registration and Authorization of Users

- **Registration:** Users can register by filling out a form with personal data (name, surname, e-mail).
- **Login:** Users can login using their login and password.
- **Logout:** Authorized users can log out of their account.

### 2. Search for Recipes

- **By Tags:** Users can find random recipes by selecting tags (e.g., vegetarian, desserts, etc.).

  ![Search for recipes by tags](images/search_recipes_by_tags.png)

- **By Ingredients:** Users can search for recipes by specifying the ingredients they have.

  ![Search for recipes by ingredients](images/search_recipes_by_ingredient.png)

- **By Nutrition:** Users can find recipes based on parameters such as minimum protein, maximum calories, minimum carbohydrates, and maximum fat.

  ![Search for recipes by nutrition](images/search_recipes_by_nutrition.png)

### 3. View Recipe Details

Users can view detailed information about a recipe, including ingredients, cooking instructions, cooking time, and number of servings.

  ![Recipe information](images/recipe_information.png)

### 4. Meal Planning

- **Adding a Recipe to a Plan:** Authorized users can add recipes (by recipe id) to their meal plan by selecting a date, slot (breakfast, lunch, dinner), and position in the plan.

  ![Adding a recipe to a plan](images/adding_recipe_to_plan.png)

  If a dish is successfully added to the user's meal plan, a message is displayed.

  ![Message](images/message_for_adding_dish.png)

- **View Weekly Plan:** Users can view their meal plan for the week and view recipes planned for specific days.

  ![View weekly plan](images/view_weekly_plan.png)

### 5. Deleting a Recipe from the Plan

Users can remove recipes from the meal plan if needed by pressing the "Remove" button on the user's weekly meal plan page.
If the meal is successfully removed from the user's meal plan, a message is displayed.

  ![Message](images/message_for_removing_dish.png)

## Technical Details

### Technology Stack:

- **Django:** Used to create a web interface and work with a database.
- **Requests:** Used to interact with Spoonacular's external API to retrieve recipes.
- **API:** The app is integrated with the Spoonacular API to retrieve recipe information. Users must obtain an API key and a host to access the API.

### Setup

#### Clone the Repository:

```bash
git clone https://github.com/VasiaBirchak/Recipe_Finder_and_Meal_Planner.git
cd recipe_planner
