"""Инициализация маршрутов для обработки ошибок в приложении"""
from flask import Blueprint

bp = Blueprint('errors', __name__, static_folder='static')

from app.errors import handlers
