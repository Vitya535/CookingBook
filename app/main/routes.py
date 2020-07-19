"""Основные маршруты приложения"""
from html import escape

from flask import current_app
from flask import jsonify
from flask import render_template
from flask import request
from htmlmin import minify

from app.forms import DishSearchForm
from app.main import bp
from app.orm_db_actions import delete_dish
from app.orm_db_actions import search_dishes
from app.utils import TypesOfDish
from app.utils import UnitsOfMeasurement


@bp.after_request
def add_header(response):
    """Функция, вставляющая после каждого запроса заголовок STS для безопасности данных"""
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.cache_control.max_age = 31536000
    return response


@bp.context_processor
def inject_common_template_params() -> dict:
    """Общая функция, необходимая для вставки общих параметров для шаблонов"""
    return dict(types_of_dish=TypesOfDish)


@bp.route('/dishes/<type_of_dishes>')
def show_dishes(type_of_dishes: str) -> str:
    """Функция показа странички для любых типов блюд"""
    current_app.logger.debug(f'Enter into {show_dishes.__name__} with params: type_of_dishes={type_of_dishes}')
    dish_search_form = DishSearchForm(request.args)
    query_title = request.args.get('dish_name', '')
    dishes_info = search_dishes(TypesOfDish[type_of_dishes.upper()], query_title)
    return minify(render_template('public/dish_page.html',
                                  units_of_measurement=UnitsOfMeasurement,
                                  selected_dish=TypesOfDish[type_of_dishes.upper()].value,
                                  type_of_dishes=type_of_dishes,
                                  dishes_info=dishes_info,
                                  dish_search_form=dish_search_form))


@bp.route('/delete', methods=['POST'])
def delete_dish_info():
    """Функция для удаления блюда из БД"""
    dish_name = escape(request.values.get('dish_name'))
    current_app.logger.debug(f'Enter into {delete_dish_info.__name__} with dish_name={dish_name}')
    delete_dish(dish_name)
    return jsonify()


@bp.route('/')
def show_first_page() -> str:
    """Функция для показа главной странички приложения"""
    current_app.logger.debug(f'Enter into {show_first_page.__name__}')
    return minify(render_template('public/first_page.html',
                                  title='Кулинарная книга'))


@bp.route('/about')
def show_about() -> str:
    """Функция для показа странички 'О приложении'"""
    current_app.logger.debug(f'Enter into {show_about.__name__}')
    return minify(render_template('public/about.html',
                                  title='О проекте'))
