"""Основной файл приложения"""
from flask import Flask, render_template
from flask_assets import Environment
from flask_csp.csp import csp_header
import sqlite_db
# from utils import *
# from datetime import datetime
# from html import escape - для экранирования (защита от XSS)

APP = Flask(__name__)
APP.config.from_pyfile('config.py')

ASSETS = Environment(APP)


@APP.route('/')
@csp_header({
    "default-src": "",
    "script-src": "",
    "img-src": "",
    "object-src": "",
    "plugin-src": "",
    "style-src": "",
    "media-src": "https://youtube.com",
    "child-src": "https://youtube.com",
    "connect-src": "",
    "base-uri": "",
    "report-uri": "/csp_report"
})
def show_content():
    """Показ содержания кулинарной книги"""
    # sqlite_db.add_dish('Жареная курица', 'Это блюдо вызовет у вас восхищение!', 8, TypesOfDish.MEAT_DISHES.value)
    # sqlite_db.add_dish('Суп', 'Этот суп просто прекрасен!', 10, TypesOfDish.LEAN_DISHES.value)
    # sqlite_db.add_recipe('static/images/1.jpg', 'https://www.russianfood.com/recipes/bytype/?fid=1454',
    # datetime(minute=20, year=DEFAULT_YEAR, month=DEFAULT_MONTH, day=DEFAULT_DAY), datetime(minute=40,
    # year=DEFAULT_YEAR, month=DEFAULT_MONTH, day=DEFAULT_DAY), 'Жареная курица') sqlite_db.add_recipe(
    # 'static/images/2.jpg', 'https://www.russianfood.com/recipes/bytype/?fid=11', datetime(minute=30,
    # year=DEFAULT_YEAR, month=DEFAULT_MONTH, day=DEFAULT_DAY), datetime(minute=50, year=DEFAULT_YEAR,
    # month=DEFAULT_MONTH, day=DEFAULT_DAY), 'Суп') sqlite_db.add_ingredient('Перец', 300,
    # UnitsOfMeasurement.GRAM.value, 'Жареная курица') sqlite_db.add_ingredient('Свинина', 500,
    # UnitsOfMeasurement.GRAM.value, 'Суп') sqlite_db.add_implement('Миска',
    # 'https://www.russianfood.com/recipes/bytype/?fid=1454') sqlite_db.add_implement('Черпак',
    # 'https://www.russianfood.com/recipes/bytype/?fid=11') sqlite_db.add_step_of_cook(1, 'ляляля',
    # 'https://www.russianfood.com/recipes/bytype/?fid=1454') sqlite_db.add_step_of_cook(2, 'тттттт',
    # 'https://www.russianfood.com/recipes/bytype/?fid=11')
    # print(sqlite_db.get_all_data_from_table('dish'))
    return render_template('table_view.html', titles=sqlite_db.get_titles(),
                           attrs=sqlite_db.get_titles_of_attrs('dish'),
                           data=sqlite_db.get_all_data_from_table('dish'))


if __name__ == '__main__':
    APP.run()
