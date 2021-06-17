import sqlite3
from consts import *
import argparse


def insert_meals(meals):
    for meal in meals:
        populate_meals = f'INSERT INTO meals(meal_name) ' \
                         f'VALUES("{meal}")'
        cursor_name.execute(populate_meals)
        conn.commit()


def insert_ingredients(ingredients):
    for ingredient in ingredients:
        populate_ingredients = f'INSERT INTO ingredients(ingredient_name) ' \
                               f'VALUES("{ingredient}")'
        cursor_name.execute(populate_ingredients)
        conn.commit()


def insert_measures(measures):
    for measure in measures:
        populate_measures = f'INSERT INTO measures(measure_name) ' \
                            f'VALUES("{measure}")'
        cursor_name.execute(populate_measures)
        conn.commit()


def insert_recipe(recipe):
    populate_recipe = f'INSERT INTO recipes(recipe_name, recipe_description) ' \
                      f'VALUES("{recipe[0]}", "{recipe[1]}")'
    cursor_name.execute(populate_recipe)
    conn.commit()


def insert_serve(meal_times, recipe_id):
    for meal_time in meal_times:
        populate_serve = f'INSERT INTO serve(meal_id, recipe_id) ' \
                         f'VALUES("{meal_time}", "{recipe_id}")'
        cursor_name.execute(populate_serve)
        conn.commit()


def store_quantity(information, recipe_id):
    information = information.split()
    quantity = int(information[0])
    if len(information) == 2:  # no measures
        measure_name = ""
        ingredient_name = information[1]
    else:
        measure_name = information[1]
        ingredient_name = information[2]

    ingredient_id_query = f'SELECT ingredient_id ' \
                          f'FROM ingredients ' \
                          f'WHERE ingredient_name LIKE "{ingredient_name}%"' \
                          f'OR ingredient_name LIKE "%{ingredient_name}"'
    ingredient_id = cursor_name.execute(ingredient_id_query).fetchall()
    if not len(ingredient_id) == 1:
        print("The ingredient is not conclusive!")
        return
    ingredient_id = ingredient_id[0][0]
    measure_id_query = f'SELECT measure_id ' \
                       f'FROM measures ' \
                       f'WHERE measure_name="{measure_name}"'
    measure_id = cursor_name.execute(measure_id_query).fetchall()
    if not len(measure_id) == 1:
        print("The ingredient is not conclusive!")
        return
    measure_id = measure_id[0][0]
    populate_quantity = f'INSERT INTO quantity(quantity, measure_id, ingredient_id, recipe_id) ' \
                        f'VALUES("{quantity}", "{measure_id}", "{ingredient_id}", "{recipe_id}")'
    cursor_name.execute(populate_quantity)
    conn.commit()


def enter_recipes():
    print("Pass the empty recipe name to exit")
    new_recipe_name = input("Recipe name: ")

    recipe_id = 0
    while new_recipe_name:
        new_recipe_descr = input("Recipe description: ")
        print("1) breakfast  2) brunch  3) lunch  4) supper")
        served_on = input("When the dish can be served:")
        served_on = [int(time) for time in served_on.split()]
        added_serve = {new_recipe_name: served_on}
        data["serves"] += (added_serve,)
        added_recipe = [new_recipe_name, new_recipe_descr]
        data["recipes"] += (added_recipe,)
        insert_recipe(added_recipe)
        recipe_id += 1
        insert_serve(served_on, recipe_id)

        quant_input = input("Input quantity of ingredient <press enter to stop>: ")
        while quant_input:
            store_quantity(quant_input, recipe_id)
            quant_input = input("Input quantity of ingredient <press enter to stop>: ")
        new_recipe_name = input("Recipe name: ")


def find_recipes(ingredients, meals):
    quantities_from_ingredient = []
    quantity_meal = []
    for ingredient in ingredients:
        ingredient_query = f'SELECT ingredient_id FROM ingredients WHERE ingredient_name = "{ingredient}"'
        recipe_id_query = f'SELECT recipe_id FROM quantity WHERE ingredient_id in ({ingredient_query})'
        recipe_ids = cursor_name.execute(recipe_id_query).fetchall()
        quantity_from_ingredient = []
        for recipe_id in recipe_ids:
            quantity_from_ingredient.append(recipe_id[0])
        quantities_from_ingredient.append(quantity_from_ingredient)
    quantity_from_ingredient = set(quantities_from_ingredient[0]).intersection(*quantities_from_ingredient)
    quantity_from_ingredient = list(quantity_from_ingredient)
    for meal in meals:
        meal_query = f'SELECT meal_id FROM meals WHERE meal_name = "{meal}"'
        recipe_id_query = f'SELECT recipe_id FROM serve WHERE meal_id in ({meal_query})'
        recipe_ids = cursor_name.execute(recipe_id_query).fetchall()
        for recipe_id in recipe_ids:
            quantity_meal.append(recipe_id[0])
    final = []
    for recipe in quantity_from_ingredient:
        if recipe in quantity_meal:
            final_query = f'SELECT recipe_name FROM recipes WHERE recipe_id={recipe}'
            final.append(cursor_name.execute(final_query).fetchone()[0])
    names = ", ".join(final)
    print(f"Recipes selected for you: {names}" if final else "There are no such recipes in the database.")


parser = argparse.ArgumentParser()
parser.add_argument("Database", help="Database name")
parser.add_argument("--ingredients", help="ingredients to search into recipe")
parser.add_argument("--meals", help="type of the meal where a recipe can be served")
args = parser.parse_args()
print(args)

if not args.ingredients:
    conn = sqlite3.connect(data_base_name)
    cursor_name = conn.cursor()
    cursor_name.execute(foreign_key)
    cursor_name.execute(meals_table)
    cursor_name.execute(ingredients_table)
    cursor_name.execute(measures_table)
    cursor_name.execute(recipes_table)
    cursor_name.execute(serve_table)
    cursor_name.execute(quantity_table)
    conn.commit()
    insert_meals(data["meals"])
    insert_ingredients(data["ingredients"])
    insert_measures(data["measures"])
    enter_recipes()
else:
    conn = sqlite3.connect(args.Database)
    cursor_name = conn.cursor()
    find_recipes(args.ingredients.split(","), args.meals.split(","))

conn.commit()
conn.close()
