"""Файл конфигурации проекта"""
from os import urandom
from os.path import dirname
from os.path import join


class Config:
    """Основной класс конфигурации"""
    APP_DB_RELPATH = 'cooking_book.db'
    TRANSLATION_DIR_RELPATH = '../translations'
    SESSION_TYPE = 'filesystem'
    WTF_CSRF_ENABLED = CDN_HTTPS = SESSION_COOKIE_HTTPONLY = True
    SECRET_KEY = JWT_SECRET_KEY = urandom(16)
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{join(dirname(__file__), APP_DB_RELPATH)}'
    CDN_TIMESTAMP = JSON_AS_ASCII = False
    CDN_DOMAIN = 'cdnjs.cloudflare.com'
    CDN_ENDPOINTS = ('ajax/libs/jquery/3.5.1/jquery.min.js',
                     'ajax/libs/twitter-bootstrap/4.5.0/js/bootstrap.min.js',
                     'ajax/libs/jquery-confirm/3.3.4/jquery-confirm.min.js',
                     'ajax/libs/twitter-bootstrap/4.5.0/css/bootstrap.min.css',
                     'ajax/libs/jquery-confirm/3.3.4/jquery-confirm.min.css')
    BABEL_DEFAULT_LOCALE = 'ru'
    LANGUAGES = ('ru', 'en')
    BABEL_TRANSLATION_DIRECTORIES = join(dirname(__file__), TRANSLATION_DIR_RELPATH)


class ProductionConfig(Config):
    """Конфигурация для выпуска в Production"""
    JSONIFY_PRETTYPRINT_REGULAR = SQLALCHEMY_TRACK_MODIFICATIONS = ASSETS_DEBUG = False


class DevelopmentConfig(Config):
    """Конфигурация для разработки"""
    SQLALCHEMY_TRACK_MODIFICATIONS = ASSETS_DEBUG = True


class TestingConfig(Config):
    """Конфигурация для тестирования"""
    TEST_DB_RELPATH = '../test/test.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{join(dirname(__file__), TEST_DB_RELPATH)}'
