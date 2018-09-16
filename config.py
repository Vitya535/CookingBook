"""Файл конфигурации проекта"""
FLASK_DEBUG = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///cooking_book.db?check_same_thread=False'
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = 'NotTellAnyone'
FLASK_ENV = 'development'
SESSION_COOKIE_HTTPONLY = True
