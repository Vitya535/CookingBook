"""Модуль базы данных sqlite для приложения"""
from sqlite3 import connect

CONN = connect('cooking_book.db')

CURSOR = CONN.cursor()

CURSOR.execute("""PRAGMA foreign_keys = ON""")

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
                FOREIGN KEY (recipe_id) REFERENCES recipe(id) ON DELETE CASCADE ON UPDATE CASCADE,
                CONSTRAINT unique_description UNIQUE (description))""")

CURSOR.execute("""CREATE TABLE if not exists recipe
                (id integer PRIMARY KEY AUTOINCREMENT,
                img_url text NOT NULL, literature_url text NOT NULL,
                time_on_preparation text CHECK (time_on_preparation>0) NOT NULL,
                time_on_cooking text CHECK (time_on_cooking>0) NOT NULL,
                dish_id integer NOT NULL,
                FOREIGN KEY (dish_id) REFERENCES dish(id) ON DELETE CASCADE ON UPDATE CASCADE,
                CONSTRAINT unique_urls UNIQUE (img_url, literature_url))""")

CURSOR.execute("""CREATE TABLE if not exists recipe_and_implement
                (recipe_id integer NOT NULL, implement_id integer NOT NULL,
                FOREIGN KEY (recipe_id) REFERENCES recipe(id) ON DELETE CASCADE ON UPDATE CASCADE,
                FOREIGN KEY (implement_id) REFERENCES implement(id) ON DELETE CASCADE ON UPDATE CASCADE,
                CONSTRAINT composite_key_2 PRIMARY KEY (recipe_id, implement_id))""")

CURSOR.execute("""CREATE TABLE if not exists dish_and_ingredient
                (dish_id integer NOT NULL, ingredient_id integer NOT NULL,
                FOREIGN KEY (dish_id) REFERENCES dish(id) ON DELETE CASCADE ON UPDATE CASCADE,
                FOREIGN KEY (ingredient_id) REFERENCES ingredient(id) ON DELETE CASCADE ON UPDATE CASCADE,
                CONSTRAINT composite_key_1 PRIMARY KEY (dish_id, ingredient_id))""")

CONN.commit()
CONN.close()

# а нужно ли утварь каскадно удалять или нет?


def add_dish(name, description, portion_count, type_of_dish):
    """Добавление блюда"""
    conn = connect('cooking_book.db')
    cursor = conn.cursor()
    cursor.execute("""PRAGMA foreign_keys = ON""")
    cursor.execute("INSERT INTO dish (name, description, portion_count, type_of_dish) VALUES(?, ?, ?, ?)",
                   (name, description, portion_count, type_of_dish,))
    conn.commit()
    conn.close()


def delete_dish(name, description):
    """Удаление блюда"""
    conn = connect('cooking_book.db')
    cursor = conn.cursor()
    cursor.execute("""PRAGMA foreign_keys = ON""")
    cursor.execute("DELETE FROM dish WHERE name==? AND description==?",
                   (name, description,))
    conn.commit()
    conn.close()


def update_dish(name, description, portion_count, type_of_dish):
    """Обновление блюда"""
    conn = connect('cooking_book.db')
    cursor = conn.cursor()
    cursor.execute("""PRAGMA foreign_keys = ON""")
    cursor.execute("UPDATE dish (name, description, portion_count, type_of_dish) "
                   "SET name=?, description=?, portion_count=?, type_of_dish=? WHERE name==? AND "
                   "description==? AND portion_count==? AND type_of_dish==?", (name, description, portion_count,
                                                                               type_of_dish,))
    conn.commit()
    conn.close()


def add_ingredient(name, count, unit_of_measurement, dish_name):
    """Добавление ингредиента"""
    conn = connect('cooking_book.db')
    cursor = conn.cursor()
    cursor.execute("""PRAGMA foreign_keys = ON""")
    cursor.execute("SELECT id FROM dish WHERE name==?", (dish_name,))
    conn.commit()
    dish_id = cursor.fetchall()[0][0]
    cursor.execute("INSERT INTO ingredient (name, count, unit_of_measurement) VALUES(?, ?, ?)",
                   (name, count, unit_of_measurement,))
    conn.commit()
    cursor.execute("SELECT id FROM ingredient WHERE name==? AND count==? AND unit_of_measurement==?",
                   (name, count, unit_of_measurement,))
    conn.commit()
    ingredient_id = cursor.fetchall()[0][0]
    cursor.execute("INSERT INTO dish_and_ingredient (dish_id, ingredient_id) VALUES(?, ?)", (dish_id, ingredient_id,))
    conn.commit()
    conn.close()


def delete_ingredient(name, count, unit_of_measurement):
    """Удаление ингредиента"""
    conn = connect('cooking_book.db')
    cursor = conn.cursor()
    cursor.execute("""PRAGMA foreign_keys = ON""")
    cursor.execute("DELETE FROM ingredient WHERE name==? AND count==? AND unit_of_measurement==?",
                   (name, count, unit_of_measurement,))
    conn.commit()
    conn.close()


def update_ingredient(name, count, unit_of_measurement):
    """Обновление ингредиента"""
    conn = connect('cooking_book.db')
    cursor = conn.cursor()
    cursor.execute("""PRAGMA foreign_keys = ON""")
    cursor.execute("UPDATE ingredient (name, count, unit_of_measurement) SET name=?, count=?, unit_of_measurement=?"
                   " WHERE name==? AND count==? AND unit_of_measurement==?", (name, count, unit_of_measurement,))
    conn.commit()
    conn.close()


def add_implement(name, recipe_url):
    """Добавление утвари"""
    conn = connect('cooking_book.db')
    cursor = conn.cursor()
    cursor.execute("""PRAGMA foreign_keys = ON""")
    cursor.execute("SELECT id FROM recipe WHERE literature_url==?", (recipe_url,))
    conn.commit()
    recipe_id = cursor.fetchall()[0][0]
    cursor.execute("INSERT INTO implement (name) VALUES(?)", (name,))
    conn.commit()
    cursor.execute("SELECT id FROM implement WHERE name==?", (name,))
    conn.commit()
    implement_id = cursor.fetchall()[0][0]
    cursor.execute("INSERT INTO recipe_and_implement (recipe_id, implement_id) VALUES(?, ?)",
                   (recipe_id, implement_id,))
    conn.commit()
    conn.close()


def delete_implement(name):
    """Удаление утвари"""
    conn = connect('cooking_book.db')
    cursor = conn.cursor()
    cursor.execute("""PRAGMA foreign_keys = ON""")
    cursor.execute("DELETE FROM implement (name) WHERE name==?", (name,))
    conn.commit()
    conn.close()


def update_implement(name):
    """Обновление утвари"""
    conn = connect('cooking_book.db')
    cursor = conn.cursor()
    cursor.execute("""PRAGMA foreign_keys = ON""")
    cursor.execute("UPDATE implement (name) SET name=? WHERE name==?", (name,))
    conn.commit()
    conn.close()


def add_recipe(img_url, literature_url, time_on_preparation, time_on_cooking, dish_name):
    """Добавление рецепта"""
    conn = connect('cooking_book.db')
    cursor = conn.cursor()
    cursor.execute("""PRAGMA foreign_keys = ON""")
    cursor.execute("SELECT id FROM dish WHERE name==?", (dish_name,))
    conn.commit()
    dish_id = cursor.fetchall()[0][0]
    cursor.execute("INSERT INTO recipe (img_url, literature_url, time_on_preparation, time_on_cooking, dish_id)"
                   " VALUES(?, ?, ?, ?, ?)",
                   (img_url, literature_url, time_on_preparation, time_on_cooking, dish_id,))
    conn.commit()
    conn.close()


def delete_recipe(img_url, literature_url):
    """Удаление рецепта"""
    conn = connect('cooking_book.db')
    cursor = conn.cursor()
    cursor.execute("""PRAGMA foreign_keys = ON""")
    cursor.execute("DELETE FROM recipe WHERE img_url==? AND literature_url==?",
                   (img_url, literature_url,))
    conn.commit()
    conn.close()


def update_recipe(img_url, literature_url, time_on_preparation, time_on_cooking, dish_name):
    """Обновление рецепта"""
    conn = connect('cooking_book.db')
    cursor = conn.cursor()
    cursor.execute("""PRAGMA foreign_keys = ON""")
    cursor.execute("SELECT id FROM dish WHERE name==?", (dish_name,))
    conn.commit()
    dish_id = cursor.fetchall()[0][0]
    cursor.execute("UPDATE recipe (img_url, literature_url, time_on_preparation, time_on_cooking, dish_id) "
                   "SET img_url=?, literature_url=?, time_on_preparation=?, time_on_cooking=?, dish_id=?"
                   " WHERE img_url==? AND literature_url==? AND time_on_preparation==?"
                   " AND time_on_cooking==? AND dish_id==?",
                   (img_url, literature_url, time_on_preparation, time_on_cooking, dish_id,))
    conn.commit()
    conn.close()


def add_step_of_cook(number, description, recipe_url):
    """Добавление шага приготовления"""
    conn = connect('cooking_book.db')
    cursor = conn.cursor()
    cursor.execute("""PRAGMA foreign_keys = ON""")
    cursor.execute("SELECT id FROM recipe WHERE literature_url==?", (recipe_url,))
    conn.commit()
    recipe_id = cursor.fetchall()[0][0]
    cursor.execute("INSERT INTO step_of_cook (number_of_step, description, recipe_id) VALUES(?, ?, ?)",
                   (number, description, recipe_id,))
    conn.commit()
    conn.close()


def delete_step_of_cook(description):
    """Удаление шага приготовления"""
    conn = connect('cooking_book.db')
    cursor = conn.cursor()
    cursor.execute("""PRAGMA foreign_keys = ON""")
    cursor.execute("DELETE FROM step_of_cook WHERE description==?", (description,))
    conn.commit()
    conn.close()


def update_step_of_cook(number, description, recipe_url):
    """Обновление шага приготовления"""
    conn = connect('cooking_book.db')
    cursor = conn.cursor()
    cursor.execute("""PRAGMA foreign_keys = ON""")
    cursor.execute("SELECT id FROM recipe WHERE literature_url==?", (recipe_url,))
    conn.commit()
    recipe_id = cursor.fetchall()[0][0]
    cursor.execute("UPDATE step_of_cook (number_of_step, description, recipe_id) "
                   "SET number=?, description=?, recipe_id=? WHERE number==?"
                   " AND description==? AND recipe_id==?", (number, description, recipe_id,))
    conn.commit()
    conn.close()


def get_searched_dishes(query):
    """Получение количества результатов поиска"""
    conn = connect('cooking_book.db')
    cursor = conn.cursor()
    cursor.execute("""PRAGMA foreign_keys = ON""")
    cursor.execute("SELECT (*) FROM dish WHERE name==?", (query,))
    conn.commit()
    fetched_data = cursor.fetchall()
    conn.close()
    return fetched_data


def get_all_dishes():
    """Получение суммарного количества блюд в базе"""
    conn = connect('cooking_book.db')
    cursor = conn.cursor()
    cursor.execute("""PRAGMA foreign_keys = ON""")
    cursor.execute("SELECT name, type_of_dish FROM dish")
    conn.commit()
    fetched_data = cursor.fetchall()
    conn.close()
    return fetched_data


def get_images_of_dishes():
    conn = connect('cooking_book.db')
    cursor = conn.cursor()
    cursor.execute("""PRAGMA foreign_keys = ON""")
    cursor.execute("SELECT img_url FROM recipe")
    conn.commit()
    fetched_data = cursor.fetchall()
    conn.close()
    return fetched_data


def get_titles():
    """Получение названий отношений"""
    conn = connect('cooking_book.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
    conn.commit()
    fetched_data = cursor.fetchall()
    conn.close()
    return fetched_data


def get_titles_of_attrs(table_name):
    """Получение названий атрибутов в отношении"""
    conn = connect('cooking_book.db')
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(" + table_name + ")")
    conn.commit()
    fetched_data = cursor.fetchall()
    conn.close()
    return fetched_data


def get_all_data_from_table(title_of_table):
    """Получение кортежей из конкретной таблицы"""
    conn = connect('cooking_book.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM " + title_of_table)
    conn.commit()
    fetched_data = cursor.fetchall()
    conn.close()
    return fetched_data

# сделать функцию которая будет выводить самые популярные рецепты
# поиск по названию блюда
# вывод некоторой статистической информации
# фильтры для количества порций, времени приготовления, подготовки, по ингредиентам, по типу блюда, по утвари
