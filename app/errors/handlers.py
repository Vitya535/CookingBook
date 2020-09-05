"""Модуль для обработки ошибок на веб-страницах"""
from flask import current_app
from flask import render_template
from flask import request
from flask_wtf.csrf import CSRFError
from htmlmin import minify

from app.constants import CSRF_ERROR_MESSAGE
from app.constants import ERROR_MESSAGE_404
from app.constants import ERROR_MESSAGE_500
from app.errors import bp


@bp.app_errorhandler(404)
def not_found_error(error):
    """Эта функция вызывает пользовательскую страницу искл-я для ошибки 404 Not Found"""
    current_app.logger.error(f'route: {request.url}, Not Found error: {error}')
    return minify(render_template('errors/404.html', ERROR_MESSAGE_404=ERROR_MESSAGE_404)), 404


@bp.app_errorhandler(500)
def internal_server_error(error):
    """Эта функция вызывает пользовательскую страницу искл-я для ошибки 500 Internal Server Error"""
    current_app.logger.error(f'route: {request.url}, Internal Server error: {error}')
    return minify(render_template('errors/500.html', ERROR_MESSAGE_500=ERROR_MESSAGE_500)), 500


@bp.app_errorhandler(CSRFError)
def handle_csrf_error(error):
    """Эта функция обрабатывает ошибку CSRF валидации"""
    current_app.logger.error(f'route: {request.url}, CSRF error: {error}')
    return minify(render_template('errors/csrf_error.html', CSRF_ERROR_MESSAGE=CSRF_ERROR_MESSAGE)), 400
