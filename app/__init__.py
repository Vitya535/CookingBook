"""Инициализация приложения и его частей"""
from flask import Flask
from flask_htmlmin import HTMLMIN
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from app.assets import ASSETS

APP = Flask(__name__)

if APP.config['ENV'] == 'production':
    APP.config.from_object('app.config.ProductionConfig')
else:
    APP.config.from_object('app.config.DevelopConfig')

ASSETS.init_app(APP)

HTMLMIN = HTMLMIN(APP)
DB = SQLAlchemy(APP)
MA = Marshmallow(APP)
CSRF = CSRFProtect(APP)

from app import server
from app import errors

# ToDo - pylint выдает ошибки
