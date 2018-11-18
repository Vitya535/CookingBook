"""Основной файл приложения"""
from html import escape
from flask import render_template, jsonify, session, request
from app import APP, csrf
from orm_db_actions import METADATA, orm_add, orm_delete, orm_update, \
    Dish, Ingredient, Implement, Recipe, StepOfCook, \
    dishes_schema, ingredients_schema, implements_schema, recipes_schema, steps_of_cook_schema


# ToDo - исправить таблицу в рецепте (ее отображение на странице)


@APP.after_request
def add_http_headers(response):
    """Добавляет HTTP заголовки к каждому запросу"""
    response.headers['X-Frame-Options'] = "SAMEORIGIN"
    response.headers['X-Content-Type-Options'] = "nosniff"
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self';" \
                                                  "script-src 'self' 'unsafe-inline';" \
                                                  "style-src 'self' 'unsafe-inline';" \
                                                  "img-src 'self';" \
                                                  "object-src 'none';" \
                                                  "media-src 'none';" \
                                                  "frame-src 'none';" \
                                                  "connect-src 'self';" \
                                                  "font-src *.google.com"
    return response


# ToDo - исправить добавление данных
@APP.route('/add_to_db', methods=['POST'])
def add_to_database():
    """Функция-обертка для добавления записи в БД"""
    orm_add(session['title_of_table'])
    return jsonify()


@APP.route('/del_from_db', methods=['POST'])
def delete_from_database():
    """Функция-обертка для удаления записи из БД"""
    delete_id = int(escape(request.json['delete_id']))
    orm_delete(delete_id, session['title_of_table'])
    return jsonify()


@APP.route('/update_from_db', methods=["POST"])
def update_in_database():
    """Функция-обертка для редактирования записи из БД"""
    value = escape(request.json['value'])
    update_id = escape(request.json['update_id'])
    attr_title = escape(request.json['attr_title'])
    orm_update(value, update_id, attr_title, session['title_of_table'])
    return jsonify()


@APP.route('/Dish', methods=['GET'])
def show_dish():
    """Показ содержания таблицы, которая выбрана из списка"""
    session['title_of_table'] = 'Dish'
    attributes = [str(col).split('.')[1] for col in METADATA.tables['Dish'].columns]
    data = Dish.query.all()
    data_result = dishes_schema.dump(data)
    return jsonify(attributes, data_result.data)


@APP.route('/Ingredient', methods=['GET'])
def show_ingredient():
    """Показ содержания таблицы, которая выбрана из списка"""
    session['title_of_table'] = 'Ingredient'
    attributes = [str(col).split('.')[1] for col in METADATA.tables['Ingredient'].columns]
    data = Ingredient.query.all()
    data_result = ingredients_schema.dump(data)
    return jsonify(attributes, data_result.data)


@APP.route('/Recipe', methods=['GET'])
def show_recipe():
    """Показ содержания таблицы, которая выбрана из списка"""
    session['title_of_table'] = 'Recipe'
    attributes = [str(col).split('.')[1] for col in METADATA.tables['Recipe'].columns]
    data = Recipe.query.all()
    data_result = recipes_schema.dump(data)
    return jsonify(attributes, data_result.data)


@APP.route('/StepOfCook', methods=['GET'])
def show_step_of_cook():
    """Показ содержания таблицы, которая выбрана из списка"""
    session['title_of_table'] = 'StepOfCook'
    attributes = [str(col).split('.')[1] for col in METADATA.tables['StepOfCook'].columns]
    data = StepOfCook.query.all()
    data_result = steps_of_cook_schema.dump(data)
    return jsonify(attributes, data_result.data)


@APP.route('/Implement', methods=['GET'])
def show_implement():
    """Показ содержания таблицы, которая выбрана из списка"""
    session['title_of_table'] = 'Implement'
    attributes = [str(col).split('.')[1] for col in METADATA.tables['Implement'].columns]
    data = Implement.query.all()
    data_result = implements_schema.dump(data)
    return jsonify(attributes, data_result.data)


@APP.route('/')
def show_init_content():
    """Показ содержания таблицы dish"""
    session['title_of_table'] = 'Dish'
    titles_of_attrs = [str(col).split('.')[1] for col in METADATA.tables['Dish'].columns]
    return render_template('table_view.html', titles=list(METADATA.tables.keys())[2:],
                           attrs=titles_of_attrs,
                           data=Dish.query.all(),
                           selected=session['title_of_table'],
                           csrf=csrf)
