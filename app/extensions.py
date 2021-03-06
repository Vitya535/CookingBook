"""Расширения, необходимые для работы приложения"""
from flask_babel import Babel
from flask_cdn import CDN
from flask_compress import Compress
from flask_login import LoginManager
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

session = Session()
db = SQLAlchemy()
csrf = CSRFProtect()
cdn = CDN()
compress = Compress()
babel = Babel()
login_manager = LoginManager()
