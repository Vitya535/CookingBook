"""Модуль базы данных sqlite для приложения"""
from sqlite3 import connect

CONN = connect('cooking_book.db')
CURSOR = CONN.cursor()

CURSOR.execute("""CREATE TABLE if not exists dish
                (id integer PRIMARY KEY AUTOINCREMENT,
                name text NOT NULL, description text NOT NULL,
                portion_count integer CHECK (portion_count>0) NOT NULL,
                type_of_dish text NOT NULL,
                CONSTRAINT unique_name_and_description UNIQUE (name, description))""")

CURSOR.execute("""CREATE TABLE if not exists ingredient
                (id integer PRIMARY KEY AUTOINCREMENT,
                name text NOT NULL, count integer CHECK (count>0),
                unit_of_measurement text)""")

CURSOR.execute("""CREATE TABLE if not exists implement
                (id integer PRIMARY KEY AUTOINCREMENT,
                name text NOT NULL,
                CONSTRAINT unique_name UNIQUE (name))""")

CURSOR.execute("""CREATE TABLE if not exists step_of_cook
                (id integer PRIMARY KEY AUTOINCREMENT,
                number_of_step integer CHECK (number_of_step>0) NOT NULL,
                description text NOT NULL, recipe_id integer NOT NULL,
                FOREIGN KEY (recipe_id) REFERENCES recipe(id),
                CONSTRAINT unique_description UNIQUE (description))""")

CURSOR.execute("""CREATE TABLE if not exists recipe
                (id integer PRIMARY KEY AUTOINCREMENT,
                img_url text NOT NULL, literature_url text NOT NULL,
                time_on_preparation text NOT NULL, time_on_cooking text NOT NULL,
                dish_id integer NOT NULL,
                FOREIGN KEY (dish_id) REFERENCES dish(id),
                CONSTRAINT unique_urls UNIQUE (img_url, literature_url))""")

CURSOR.execute("""CREATE TABLE if not exists recipe_and_implement
                (recipe_id integer NOT NULL, implement_id integer NOT NULL,
                FOREIGN KEY (recipe_id) REFERENCES recipe(id),
                FOREIGN KEY (implement_id) REFERENCES implement(id),
                CONSTRAINT composite_key_2 PRIMARY KEY (recipe_id, implement_id))""")

CURSOR.execute("""CREATE TABLE if not exists dish_and_ingredient
                (dish_id integer NOT NULL, ingredient_id integer NOT NULL,
                FOREIGN KEY (dish_id) REFERENCES dish(id),
                FOREIGN KEY (ingredient_id) REFERENCES ingredient(id),
                CONSTRAINT composite_key_1 PRIMARY KEY (dish_id, ingredient_id))""")

CONN.commit()
CONN.close()


def add_dish(name, description, portion_count, type_of_dish):
    """Добавление блюда"""
    conn = connect('cooking_book.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO dish (name, description, portion_count, type_of_dish) VALUES(?, ?, ?, ?)",
                   (name, description, portion_count, type_of_dish,))
    conn.commit()
    conn.close()


def delete_dish(name, description, portion_count, type_of_dish):
    """Удаление блюда"""
    conn = connect('cooking_book.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM dish (name, description, portion_count, type_of_dish) WHERE name==? AND description==?"
                   " AND portion_count==? AND type_of_dish==?",
                   (name, description, portion_count, type_of_dish,))
    conn.commit()
    conn.close()


def update_dish(name, description, portion_count, type_of_dish):
    """Обновление блюда"""
    conn = connect('cooking_book.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE dish (name, description, portion_count, type_of_dish) "
                   "SET name=?, description=?, portion_count=?, type_of_dish=? WHERE name==? AND "
                   "description==? AND portion_count==? AND type_of_dish==?", (name, description, portion_count,
                                                                               type_of_dish,))
    conn.commit()
    conn.close()


def add_ingredient(name, count, unit_of_measurement):
    """Добавление ингредиента"""
    conn = connect('cooking_book.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ingredient (name, count, unit_of_measurement) VALUES(?, ?, ?)",
                   (name, count, unit_of_measurement,))
    conn.commit()
    conn.close()


def delete_ingredient(name, count, unit_of_measurement):
    """Удаление ингредиента"""
    conn = connect('cooking_book.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ingredient (name, count, unit_of_measurement) WHERE name==? AND count==? AND "
                   "unit_of_measurement==?",
                   (name, count, unit_of_measurement,))
    conn.commit()
    conn.close()


def update_ingredient(name, count, unit_of_measurement):
    """Обновление ингредиента"""
    conn = connect('cooking_book.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE dish (name, count, unit_of_measurement) SET name=?, count=?, unit_of_measurement=?"
                   " WHERE name==? AND count==? AND unit_of_measurement==?", (name, count, unit_of_measurement,))
    conn.commit()
    conn.close()


def add_implement(name):
    """Добавление утвари"""
    conn = connect('cooking_book.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO implement (name) VALUES(?)", (name,))
    conn.commit()
    conn.close()


def delete_implement(name):
    """Удаление утвари"""
    conn = connect('cooking_book.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM implement (name) WHERE name==?", (name,))
    conn.commit()
    conn.close()


def update_implement(name):
    """Обновление утвари"""
    conn = connect('cooking_book.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE implement (name) SET name=? WHERE name==?", (name,))
    conn.commit()
    conn.close()


def add_recipe(img_url, literature_url, time_on_preparation, time_on_cooking, dish_id):
    # нужен ли здесь dish_id?
    """Добавление рецепта"""
    conn = connect('cooking_book.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO recipe (img_url, literature_url, time_on_preparation, time_on_cooking, dish_id)"
                   " VALUES(?, ?, ?, ?, ?)",
                   (img_url, literature_url, time_on_preparation, time_on_cooking, dish_id,))
    conn.commit()
    conn.close()


def delete_recipe(img_url, literature_url, time_on_preparation, time_on_cooking, dish_id):
    """Удаление рецепта"""
    conn = connect('cooking_book.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM recipe (img_url, literature_url, time_on_preparation, time_on_cooking, dish_id) "
                   "WHERE img_url==? AND literature_url==? AND time_preparation==?"
                   " AND time_on_cooking==? AND dish_id==?",
                   (img_url, literature_url, time_on_preparation, time_on_cooking, dish_id,))
    conn.commit()
    conn.close()


def update_recipe(img_url, literature_url, time_on_preparation, time_on_cooking, dish_id):
    """Обновление рецепта"""
    conn = connect('cooking_book.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE recipe (img_url, literature_url, time_on_preparation, time_on_cooking, dish_id) "
                   "SET img_url=?, literature_url=?, time_on_preparation=?, time_on_cooking=?, dish_id=?"
                   " WHERE img_url==? AND literature_url==? AND time_on_preparation==?"
                   " AND time_on_cooking==? AND dish_id==?",
                   (img_url, literature_url, time_on_preparation, time_on_cooking, dish_id,))
    conn.commit()
    conn.close()


def add_step_of_cook(number, description, recipe_id):  # нужен ли здесь recipe_id?
    """Добавление шага приготовления"""
    conn = connect('cooking_book.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO step_of_cook (number_of_step, description, recipe_id) VALUES(?, ?, ?)",
                   (number, description, recipe_id,))
    conn.commit()
    conn.close()


def delete_step_of_cook(number, description, recipe_id):
    """Удаление шага приготовления"""
    conn = connect('cooking_book.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM step_of_cook (number_of_step, description, recipe_id) "
                   "WHERE number==? AND description==? AND recipe_id==?",
                   (number, description, recipe_id,))
    conn.commit()
    conn.close()


def update_step_of_cook(number, description, recipe_id):
    """Обновление шага приготовления"""
    conn = connect('cooking_book.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE step_of_cook (number_of_step, description, recipe_id) "
                   "SET number=?, description=?, recipe_id=? WHERE number==?"
                   " AND description==? AND recipe_id==?", (number, description, recipe_id,))
    conn.commit()
    conn.close()


def get_searched_dishes(query):
    """Получение количества результатов поиска"""
    conn = connect('cooking_book.db')
    cursor = conn.cursor()
    cursor.execute("SELECT (*) FROM dish WHERE name==?", (query,))
    conn.commit()
    fetched_data = cursor.fetchall()
    conn.close()
    return fetched_data


def get_all_dishes():
    """Получение суммарного количества блюд в базе"""
    conn = connect('cooking_book.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, type_of_dish FROM dish")
    conn.commit()
    fetched_data = cursor.fetchall()
    conn.close()
    return fetched_data


def get_images_of_dishes():
    conn = connect('cooking_book.db')
    cursor = conn.cursor()
    cursor.execute("SELECT img_url FROM recipe")
    conn.commit()
    fetched_data = cursor.fetchall()
    conn.close()
    return fetched_data

# сделать функцию которая будет выводить самые популярные рецепты
# поиск по названию блюда
# вывод некоторой статистической информации
# фильтры для количества порций, времени приготовления, подготовки, по ингредиентам, по типу блюда, по утвари
