"""Модуль для обработки ошибок на веб-страницах"""
from flask import render_template
from flask import request
from flask_wtf.csrf import CSRFError

from app import APP


@APP.errorhandler(404)
def not_found_error(error):
    """Эта функция вызывает пользовательскую страницу искл-я для ошибки 404 Not Found"""
    APP.logger.error(f"route: {request.url}, Not Found error: {error}")
    return render_template('errors/404.html'), 404


@APP.errorhandler(500)
def internal_server_error(error):
    """Эта функция вызывает пользовательскую страницу искл-я для ошибки 500 Internal Server Error"""
    APP.logger.error(f"route: {request.url}, Internal Server error: {error}")
    return render_template('errors/500.html'), 500


@APP.errorhandler(CSRFError)
def handle_csrf_error(error):
    """Эта функция обрабатывает ошибку CSRF валидации"""
    APP.logger.error(f"route: {request.url}, CSRF error: {error}")
    return render_template('errors/csrf_error.html'), 400

# ToDo - pylint выдает ошибки
