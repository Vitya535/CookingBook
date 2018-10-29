"""Точка входа в приложение"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from assets import ASSETS

APP = Flask(__name__)
APP.config.from_object('config.DevelopConfig')
ASSETS.init_app(APP)

db = SQLAlchemy(APP)
dtb = DebugToolbarExtension(APP)

from server import *

if __name__ == '__main__':
    from errors import *
    APP.run()
