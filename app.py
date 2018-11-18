"""Точка входа в приложение"""
from flask import Flask
from flask_htmlmin import HTMLMIN
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from flask_marshmallow import Marshmallow
from assets import ASSETS
from webbrowser import open

APP = Flask(__name__)
APP.config.from_object('config.DevelopConfig')
ASSETS.init_app(APP)

htmlmin = HTMLMIN(APP)
db = SQLAlchemy(APP)
ma = Marshmallow(APP)
csrf = CSRFProtect(APP)
dtb = DebugToolbarExtension(APP)

from server import *

if __name__ == '__main__':
    from errors import *
    open('http://127.0.0.1:5000')
    APP.run()
