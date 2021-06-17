data_base_name = 'food_blog.db'

foreign_key = "PRAGMA foreign_keys = ON;"

meals_table = """CREATE TABLE IF NOT EXISTS meals(
meal_id integer PRIMARY KEY,
meal_name text UNIQUE NOT NULL
);"""

ingredients_table = """CREATE TABLE IF NOT EXISTS ingredients(
ingredient_id integer PRIMARY KEY,
ingredient_name text UNIQUE NOT NULL
);"""

measures_table = """CREATE TABLE IF NOT EXISTS measures(
measure_id integer PRIMARY KEY,
measure_name text UNIQUE
);"""

recipes_table = """CREATE TABLE IF NOT EXISTS recipes(
recipe_id integer PRIMARY KEY,
recipe_name text NOT NULL,
recipe_description text
);"""

serve_table = """CREATE TABLE IF NOT EXISTS serve(
serve_id integer PRIMARY KEY,
meal_id integer NOT NULL,
recipe_id integer NOT NULL,
FOREIGN KEY (meal_id)
REFERENCES meals(meal_id),
FOREIGN KEY(recipe_id)
REFERENCES recipes(recipe_id)
);"""

quantity_table = """CREATE TABLE IF NOT EXISTS quantity(
quantity_id integer PRIMARY KEY,
quantity integer NOT NULL,
measure_id integer NOT NULL,
ingredient_id integer NOT NULL,
recipe_id integer NOT NULL,
FOREIGN KEY (measure_id)
REFERENCES measures(measure_id),
FOREIGN KEY(ingredient_id)
REFERENCES ingredients(ingredient_id),
FOREIGN KEY(recipe_id)
REFERENCES recipes(recipe_id)
);"""

data = {"meals": ("breakfast", "brunch", "lunch", "supper"),
        "ingredients": ("milk", "cacao", "strawberry", "blueberry", "blackberry", "sugar"),
        "measures": ("ml", "g", "l", "cup", "tbsp", "tsp", "dsp", ""),
        "recipes": (),
        "serves": (),
        "quantity": ()}
        #serves = ({'Milkshake': [1, 3, 4]}, {'Hot cacao': [1]}, {'Fruit salad': [3, 4]})
        #quantity = ([1, tb, sugar])
