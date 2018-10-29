"""Модуль для обработки ошибок на веб-страницах"""
from flask import render_template
from server import APP


@APP.errorhandler(404)
def not_found_error(error):
    """Эта функция вызывает пользовательскую страницу искл-я для ошибки 404 Not Found"""
    return render_template('404.html'), 404


@APP.errorhandler(500)
def internal_server_error(error):
    """Эта функция вызывает пользовательскую страницу искл-я для ошибки 500 Internal Server Error"""
    return render_template('500.html'), 500
