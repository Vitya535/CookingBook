"""Основной файл приложения"""
from html import escape
from flask import render_template, jsonify, session, request
from htmlmin.main import minify
from app import APP
from orm_db_actions import METADATA, orm_add, orm_delete, orm_update
from orm_db_actions import Dish, Ingredient, Implement, Recipe, StepOfCook, RecipeAndImplement, DishAndIngredient

# ToDo - поменять methods во всех route


@APP.after_request
def add_http_headers(response):
    """Добавляет HTTP заголовки к каждому запросу"""
    response.headers['X-Frame-Options'] = "SAMEORIGIN"
    response.headers['X-Content-Type-Options'] = "nosniff"
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "object-src 'none'," \
                                                  "media-src 'none'," \
                                                  "frame-src 'none'," \
                                                  "font-src *.google.com,"
    return response


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


@APP.route('/<path:selected_option>', methods=["POST"])
def show_select_content(selected_option):
    """Показ содержания таблицы, которая выбрана из списка"""
    session['title_of_table'] = escape(selected_option)
    attributes = [str(col).split('.')[1] for col in METADATA.tables[session['title_of_table']].columns]
    data = eval(session['title_of_table']).query.all()
    return jsonify(attributes, data)


@APP.route('/')
def show_init_content():
    """Показ содержания таблицы dish"""
    session['title_of_table'] = 'Dish'
    titles_of_attrs = [str(col).split('.')[1] for col in METADATA.tables['Dish'].columns]
    template = render_template('table_view.html', titles=METADATA.tables.keys(),
                               attrs=titles_of_attrs,
                               data=Dish.query.all(),
                               selected=session['title_of_table'])
    return minify(template, remove_all_empty_space=True)
