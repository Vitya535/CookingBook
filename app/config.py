"""Файл конфигурации проекта"""
from os import urandom
from os.path import dirname
from os.path import join


class Config:
    """Основной класс конфигурации"""
    SESSION_TYPE = 'filesystem'
    WTF_CSRF_ENABLED = CDN_HTTPS = SESSION_COOKIE_HTTPONLY = True
    SECRET_KEY = urandom(16)
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{join(dirname(__file__), "cooking_book.db")}'
    CDN_TIMESTAMP = False
    CDN_DOMAIN = 'cdnjs.cloudflare.com'
    CDN_ENDPOINTS = ('ajax/libs/jquery/3.5.1/jquery.min.js',
                     'ajax/libs/twitter-bootstrap/5.0.0-alpha1/js/bootstrap.min.js',
                     'ajax/libs/popper.js/2.4.2/umd/popper.min.js',
                     'ajax/libs/jquery-confirm/3.3.4/jquery-confirm.min.js',
                     'ajax/libs/font-awesome/5.13.1/js/fontawesome.min.js',
                     'ajax/libs/font-awesome/5.13.1/js/solid.min.js',
                     'ajax/libs/twitter-bootstrap/5.0.0-alpha1/css/bootstrap.min.css',
                     'ajax/libs/jquery-confirm/3.3.4/jquery-confirm.min.css',
                     'ajax/libs/font-awesome/5.13.1/css/solid.min.css')


class ProductionConfig(Config):
    """Конфигурация для выпуска в Production"""
    JSONIFY_PRETTYPRINT_REGULAR = SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """Конфигурация для разработки"""
    SQLALCHEMY_TRACK_MODIFICATIONS = True
