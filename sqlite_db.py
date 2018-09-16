"""Модуль базы данных sqlite для приложения"""
from sqlite3 import connect
from utils import TypesOfDish, UnitsOfMeasurement

CONN = connect('cooking_book.db')
CURSOR = CONN.cursor()

CURSOR.execute("""CREATE TABLE if not exists dishes
                (id integer PRIMARY KEY AUTOINCREMENT,
                name text NOT NULL, description text NOT NULL,
                portion_count integer CHECK (portion_count>0) NOT NULL,
                type_of_dish text NOT NULL,
                CONSTRAINT unique_name_and_description UNIQUE (name, description))""")

CURSOR.execute("""CREATE TABLE if not exists ingredients
                (id integer PRIMARY KEY AUTOINCREMENT,
                name text NOT NULL, count integer CHECK (count>0),
                unit_of_measurement text)""")

CURSOR.execute("""CREATE TABLE if not exists implements
                (id integer PRIMARY KEY AUTOINCREMENT,
                name text NOT NULL,
                CONSTRAINT unique_name UNIQUE (name))""")

CURSOR.execute("""CREATE TABLE if not exists step_of_cook
                (id integer PRIMARY KEY AUTOINCREMENT,
                number_of_step integer CHECK (number_of_step>0) NOT NULL,
                description text NOT NULL, recipe_id integer NOT NULL,
                FOREIGN KEY (recipe_id) REFERENCES recipes(id),
                CONSTRAINT unique_description UNIQUE (description))""")

CURSOR.execute("""CREATE TABLE if not exists recipes
                (id integer PRIMARY KEY AUTOINCREMENT,
                img_url text NOT NULL, literature_url text NOT NULL,
                time_on_preparation text NOT NULL, time_on_cooking text NOT NULL,
                dish_id integer NOT NULL,
                FOREIGN KEY (dish_id) REFERENCES dishes(id),
                CONSTRAINT unique_urls UNIQUE (img_url, literature_url))""")

CURSOR.execute("""CREATE TABLE if not exists recipes_and_implements
                (recipe_id integer NOT NULL, implement_id integer NOT NULL,
                FOREIGN KEY (recipe_id) REFERENCES recipes(id),
                FOREIGN KEY (implement_id) REFERENCES implements(id),
                CONSTRAINT composite_key_2 PRIMARY KEY (recipe_id, implement_id))""")

CURSOR.execute("""CREATE TABLE if not exists dishes_and_ingredients
                (dish_id integer NOT NULL, ingredient_id integer NOT NULL,
                FOREIGN KEY (dish_id) REFERENCES dishes(id),
                FOREIGN KEY (ingredient_id) REFERENCES ingredients(id),
                CONSTRAINT composite_key_1 PRIMARY KEY (dish_id, ingredient_id))""")

CONN.commit()
CONN.close()


def add_dish(arg_id, name, description, portion_count, type_of_dish):
    """Добавление блюда"""
    conn = connect('cooking_book.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO dishes VALUES(?, ?, ?, ?, ?)", (arg_id, name, description, portion_count,
                                                                type_of_dish,))
    conn.commit()
    conn.close()


def delete_dish(arg_id, name, description, portion_count, type_of_dish):
    """Удаление блюда"""
    conn = connect('cooking_book.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM dishes WHERE arg_id==? AND name==? AND description==? AND portion_count==?"
                   " AND type_of_dish==?", (arg_id, name, description, portion_count, type_of_dish,))
    conn.commit()
    conn.close()


def update_dish(arg_id, name, description, portion_count, type_of_dish):
    """Обновление блюда"""
    conn = connect('cooking_book.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE dishes SET name=?, description=?, portion_count=?, type_of_dish=? WHERE arg_id==?"
                   " AND name==? AND description==? AND portion_count==? AND "
                   "type_of_dish==?", (arg_id, name, description, portion_count, type_of_dish,))
    conn.commit()
    conn.close()


def add_ingredient(arg_id, name, count, unit_of_measurement):
    """Добавление ингредиента"""
    conn = connect('cooking_book.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ingredients VALUES(?, ?, ?, ?)", (arg_id, name, count, unit_of_measurement,))
    conn.commit()
    conn.close()


def delete_ingredient(arg_id, name, count, unit_of_measurement):
    """Удаление ингредиента"""
    conn = connect('cooking_book.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ingredients WHERE arg_id==? AND name==? AND count==? AND unit_of_measurement==?",
                   (arg_id, name, count, unit_of_measurement,))
    conn.commit()
    conn.close()


def update_ingredient(arg_id, name, count, unit_of_measurement):
    """Обновление ингредиента"""
    conn = connect('cooking_book.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE dishes SET name=?, count=?, unit_of_measurement=? WHERE arg_id==? AND name==?"
                   " AND count==? AND unit_of_measurement==?", (arg_id, name, count, unit_of_measurement,))
    conn.commit()
    conn.close()


def add_implement(arg_id, name):
    """Добавление утвари"""
    conn = connect('cooking_book.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO implements VALUES(?, ?)", (arg_id, name,))
    conn.commit()
    conn.close()


def delete_implement(arg_id, name):
    """Удаление утвари"""
    conn = connect('cooking_book.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM implements WHERE arg_id==? AND name==?", (arg_id, name,))
    conn.commit()
    conn.close()


def update_implement(arg_id, name):
    """Обновление утвари"""
    conn = connect('cooking_book.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE implements SET name=? WHERE arg_id==? AND name==?", (arg_id, name,))
    conn.commit()
    conn.close()


def add_recipe(arg_id, img_url, literature_url, time_on_preparation, time_on_cooking, dish_id):
    # нужен ли здесь dish_id?
    """Добавление рецепта"""
    conn = connect('cooking_book.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO recipes VALUES(?, ?, ?, ?, ?, ?)",
                   (arg_id, img_url, literature_url, time_on_preparation, time_on_cooking, dish_id,))
    conn.commit()
    conn.close()


def delete_recipe(arg_id, img_url, literature_url, time_on_preparation, time_on_cooking, dish_id):
    """Удаление рецепта"""
    conn = connect('cooking_book.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM recipes WHERE arg_id==? AND img_url==? AND literature_url==? AND time_preparation==?"
                   " AND time_on_cooking==? AND dish_id==?",
                   (arg_id, img_url, literature_url, time_on_preparation, time_on_cooking, dish_id,))
    conn.commit()
    conn.close()


def update_recipe(arg_id, img_url, literature_url, time_on_preparation, time_on_cooking, dish_id):
    """Обновление рецепта"""
    conn = connect('cooking_book.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE recipes SET img_url=?, literature_url=?, time_on_preparation=?, time_on_cooking=?, dish_id=?"
                   " WHERE arg_id==? AND img_url==? AND literature_url==? AND time_on_preparation==?"
                   " AND time_on_cooking==? AND dish_id==?",
                   (arg_id, img_url, literature_url, time_on_preparation, time_on_cooking, dish_id,))
    conn.commit()
    conn.close()


def add_step_of_cook(arg_id, number, description, recipe_id):  # нужен ли здесь recipe_id?
    """Добавление шага приготовления"""
    conn = connect('cooking_book.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO step_of_cook VALUES(?, ?, ?, ?)", (arg_id, number, description, recipe_id,))
    conn.commit()
    conn.close()


def delete_step_of_cook(arg_id, number, description, recipe_id):
    """Удаление шага приготовления"""
    conn = connect('cooking_book.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM step_of_cook WHERE arg_id==? AND number==? AND description==? AND recipe_id==?",
                   (arg_id, number, description, recipe_id,))
    conn.commit()
    conn.close()


def update_step_of_cook(arg_id, number, description, recipe_id):
    """Обновление шага приготовления"""
    conn = connect('cooking_book.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE step_of_cook SET number=?, description=?, recipe_id=? WHERE arg_id==? AND number==?"
                   " AND description==? AND recipe_id==?", (arg_id, number, description, recipe_id,))
    conn.commit()
    conn.close()


def get_searched_dishes(query):
    """Получение количества результатов поиска"""
    conn = connect('cooking_book.db')
    cursor = conn.cursor()
    cursor.execute("SELECT (*) FROM dishes WHERE name==?", (query,))
    conn.commit()
    return cursor.fetchall()  # закрыть бы базу


def get_all_dishes():
    """Получение суммарного количества блюд в базе"""
    conn = connect('cooking_book.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, type_of_dish FROM dishes")
    conn.commit()
    return cursor.fetchall()  # закрыть бы базу


def get_images_of_dishes():
    conn = connect('cooking_book.db')
    cursor = conn.cursor()
    cursor.execute("SELECT img_url FROM recipes")
    conn.commit()
    return cursor.fetchall()  # закрыть бы базу

# сделать функцию которая будет выводить самые популярные рецепты
# поиск по названию блюда
# вывод некоторой статистической информации
# фильтры для количества порций, времени приготовления, подготовки, по ингредиентам, по типу блюда, по утвари
