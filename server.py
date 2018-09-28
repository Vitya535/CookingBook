"""Основной файл приложения"""
from flask import Flask, render_template
from flask_assets import Environment
from flask_csp.csp import csp_header
import sqlite_db
# from html import escape - для экранирования (защита от XSS)

APP = Flask(__name__)
APP.config.from_pyfile('config.py')

ASSETS = Environment(APP)


@APP.route('/<path:selected_option>')
def show_select_content(selected_option):
    """Показ содержания таблицы, которая выбрана из списка"""
    return render_template('table_view.html', selected=selected_option, titles=sqlite_db.get_titles(),
                           attrs=sqlite_db.get_titles_of_attrs(selected_option),
                           data=sqlite_db.get_all_data_from_table(selected_option))


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
def show_init_content():
    """Показ содержания таблицы dish"""
    return render_template('table_view.html', titles=sqlite_db.get_titles(),
                           attrs=sqlite_db.get_titles_of_attrs('dish'),
                           data=sqlite_db.get_all_data_from_table('dish'))


if __name__ == '__main__':
    APP.run()
