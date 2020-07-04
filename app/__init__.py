"""Инициализация приложения и его частей"""
from flask import Flask
from flask_cdn import CDN
from flask_compress import Compress
from flask_marshmallow import Marshmallow
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from app.assets import ASSETS
from app.security import CSP
from app.security import TALISMAN

APP = Flask(__name__)

APP.config.from_object(f'app.config.{APP.config["ENV"]}Config')

ASSETS.init_app(APP)

SESSION = Session(APP)
DB = SQLAlchemy(APP)
MA = Marshmallow(APP)
CSRF = CSRFProtect(APP)
CDN = CDN(APP)
COMPRESS = Compress(APP)
TALISMAN.init_app(APP, content_security_policy=CSP, force_https=False)

from app.views import *
from app.errors import *
