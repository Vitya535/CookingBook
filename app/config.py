"""Файл конфигурации проекта"""
from os import path

BASEDIR = path.abspath(path.dirname(__file__))


class Config:
    """Основной класс конфигурации"""
    DEBUG = False
    CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = 'dffgrtrw45'
    SECRET_KEY = 'NotTellAnyone'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(BASEDIR, 'cooking_book.db')
    SESSION_COOKIE_HTTPONLY = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    MINIFY_PAGE = True


class ProductionConfig(Config):
    """Конфигурация для выпуска в Production"""
    ASSETS_DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopConfig(Config):
    """Конфигурация для отладки"""
    DEBUG = True
    ASSETS_DEBUG = True

# ToDo - pylint выдает ошибки
