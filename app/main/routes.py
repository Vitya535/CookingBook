"""Основные маршруты приложения"""
from flask import Markup
from flask import current_app
from flask import jsonify
from flask import render_template
from flask import request
from flask_babel import gettext
from flask_login import current_user
from htmlmin import minify

from app.constants import ABOUT_PROJECT_1
from app.constants import ABOUT_PROJECT_2
from app.constants import ADD_DISH
from app.constants import AUTHOR
from app.constants import COOKING_BOOK
from app.constants import COOKING_TIME
from app.constants import DELETE_DISH
from app.constants import DESCRIPTION
from app.constants import DISHES
from app.constants import DISH_IMAGE
from app.constants import FIRST_PAGE_CONTENT
from app.constants import IMPLEMENT
from app.constants import INGREDIENTS
from app.constants import LANGUAGE
from app.constants import LITERATURE_URL
from app.constants import LOGIN
from app.constants import LOGOUT
from app.constants import MY_DISHES
from app.constants import PORTIONS_COUNT
from app.constants import PREPARATION_TIME
from app.constants import RECIPE_FROM_BOOKS_AND_INTERNET
from app.constants import REGISTRATION
from app.constants import STEP_OF_COOK
from app.constants import WELCOME_TO_COOKING_BOOK
from app.forms import DishSearchForm
from app.main import bp
from app.orm_db_actions import delete_dish
from app.orm_db_actions import search_dishes
from app.utils import TypesOfDish
from app.utils import UnitsOfMeasurement


@bp.context_processor
def inject_common_template_params() -> dict:
    """Общая функция, необходимая для вставки общих параметров для шаблонов"""
    return dict(types_of_dish=TypesOfDish,
                COOKING_BOOK=COOKING_BOOK,
                DISHES=DISHES,
                ABOUT_PROJECT_2=ABOUT_PROJECT_2,
                LOGIN=LOGIN,
                MY_DISHES=MY_DISHES,
                ADD_DISH=ADD_DISH,
                LANGUAGE=LANGUAGE,
                LOGOUT=LOGOUT,
                REGISTRATION=REGISTRATION)


@bp.route('/dishes/<type_of_dishes>')
def show_dishes(type_of_dishes: str) -> str:
    """Функция показа странички для любых типов блюд"""
    current_app.logger.debug(f'Enter into {show_dishes.__name__} with params: type_of_dishes={type_of_dishes}')
    dish_search_form = DishSearchForm(request.args)
    query_title = request.args.get('dish_name', '')
    dishes_info = search_dishes(TypesOfDish[type_of_dishes.upper()], query_title)
    return minify(render_template('main/dish_page.html',
                                  current_user=current_user,
                                  units_of_measurement=UnitsOfMeasurement,
                                  selected_dish=TypesOfDish[type_of_dishes.upper()].value,
                                  type_of_dishes=type_of_dishes,
                                  dishes_info=dishes_info,
                                  dish_search_form=dish_search_form,
                                  PORTIONS_COUNT=PORTIONS_COUNT,
                                  DELETE_DISH=DELETE_DISH,
                                  DISH_IMAGE=DISH_IMAGE,
                                  DESCRIPTION=DESCRIPTION,
                                  PREPARATION_TIME=PREPARATION_TIME,
                                  COOKING_TIME=COOKING_TIME,
                                  LITERATURE_URL=LITERATURE_URL,
                                  IMPLEMENT=IMPLEMENT,
                                  STEP_OF_COOK=STEP_OF_COOK,
                                  INGREDIENTS=INGREDIENTS))


@bp.route('/delete', methods=['POST'])
def delete_dish_info():
    """Функция для удаления блюда из БД"""
    dish_name = request.values.get('dish_name')
    current_app.logger.debug(f'Enter into {delete_dish_info.__name__} with dish_name={dish_name}')
    delete_dish(dish_name)
    return jsonify()


@bp.route('/')
def show_first_page() -> str:
    """Функция для показа главной странички приложения"""
    current_app.logger.debug(f'Enter into {show_first_page.__name__}')
    return minify(render_template('main/first_and_about_page.html',
                                  current_user=current_user,
                                  title=COOKING_BOOK,
                                  content=Markup(f'{gettext(WELCOME_TO_COOKING_BOOK)}'
                                                 f'<p class="h5">{gettext(FIRST_PAGE_CONTENT)}</p>')))


@bp.route('/about')
def show_about() -> str:
    """Функция для показа странички 'О приложении'"""
    current_app.logger.debug(f'Enter into {show_about.__name__}')
    return minify(render_template('main/first_and_about_page.html',
                                  title=ABOUT_PROJECT_2,
                                  content=Markup(f'{gettext(ABOUT_PROJECT_1)}'
                                                 f'<p class="h5">{gettext(RECIPE_FROM_BOOKS_AND_INTERNET)}</p>'
                                                 f'<p class="h5">{gettext(AUTHOR)}</p>')))
