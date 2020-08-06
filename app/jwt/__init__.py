"""Инициализация маршрутов для авторизации/аутентификации через JWT в приложении"""
from flask import Blueprint

bp = Blueprint('jwt', __name__, static_folder='static')

from app.jwt import routes
