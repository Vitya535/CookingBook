"""Модуль для обработки ошибок на веб-страницах"""
from flask import current_app
from flask import render_template
from flask import request
from flask_wtf.csrf import CSRFError
from htmlmin import minify

from app.errors import bp


@bp.app_errorhandler(404)
def not_found_error(error):
    """Эта функция вызывает пользовательскую страницу искл-я для ошибки 404 Not Found"""
    current_app.logger.error(f'route: {request.url}, Not Found error: {error}')
    return minify(render_template('errors/404.html')), 404


@bp.app_errorhandler(500)
def internal_server_error(error):
    """Эта функция вызывает пользовательскую страницу искл-я для ошибки 500 Internal Server Error"""
    current_app.logger.error(f'route: {request.url}, Internal Server error: {error}')
    return minify(render_template('errors/500.html')), 500


@bp.app_errorhandler(CSRFError)
def handle_csrf_error(error):
    """Эта функция обрабатывает ошибку CSRF валидации"""
    current_app.logger.error(f'route: {request.url}, CSRF error: {error}')
    return minify(render_template('errors/csrf_error.html')), 400
