"""Основной файл приложения"""
from flask import Flask, render_template
from flask_assets import Environment
from flask_csp.csp import csp_header
import sqlite_db
# from utils import UnitsOfMeasurement, TypesOfDish
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
    # sqlite_db.add_implement('Миска')
    # sqlite_db.add_implement('Черпак')
    # sqlite_db.add_dish('Жареная курица', 'Это блюдо вызовет у вас восхищение!', 8, TypesOfDish.MEAT_DISHES.value)
    # sqlite_db.add_dish('Суп', 'Этот суп просто прекрасен!', 10, TypesOfDish.LEAN_DISHES.value)
    # sqlite_db.add_ingredient('Перец', 300, UnitsOfMeasurement.GRAM.value)
    # sqlite_db.add_ingredient('Свинина', 500, UnitsOfMeasurement.GRAM.value)
    # sqlite_db.add_step_of_cook(1, 'ляляля', 1)
    # sqlite_db.add_step_of_cook(2, 'тттттт', 2)
    # sqlite_db.add_recipe('static/images/1.jpg', 'https://www.russianfood.com/recipes/bytype/?fid=1454', 20, 40, 1)
    # sqlite_db.add_recipe('static/images/2.jpg', 'https://www.russianfood.com/recipes/bytype/?fid=11', 30, 50, 2)
    return render_template('content.html', dishes=sqlite_db.get_all_dishes(),
                           images_url=sqlite_db.get_images_of_dishes())


if __name__ == '__main__':
    APP.run()
