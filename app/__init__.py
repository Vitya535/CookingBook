"""Инициализация приложения и его частей"""
from logging import DEBUG
from logging import ERROR
from logging import Formatter
from logging.handlers import RotatingFileHandler
from os.path import dirname

from flask import Flask
from flask import current_app
from flask import request
from flask.logging import create_logger

from app.api import api
from app.assets import ASSETS
from app.errors import bp as errors_bp
from app.extensions import babel
from app.extensions import cdn
from app.extensions import compress
from app.extensions import csrf
from app.extensions import db
from app.extensions import jwt_manager
from app.extensions import session
from app.jwt import bp as jwt_bp
from app.main import bp as main_bp
from app.security import CSP
from app.security import TALISMAN


def create_app():
    """Функция, реализующая паттерн Application Factory
    (нужна для создания экземпляра приложения с нужной конфигурацией)"""
    app = Flask(__name__)
    app.config.from_object(f'app.config.{app.config["ENV"]}Config')

    app.register_blueprint(main_bp)
    app.register_blueprint(jwt_bp)
    app.register_blueprint(errors_bp)

    init_logs(app)

    ASSETS.init_app(app)
    session.init_app(app)
    db.init_app(app)
    csrf.init_app(app)
    cdn.init_app(app)
    compress.init_app(app)
    babel.init_app(app)
    api.init_app(app)
    jwt_manager.init_app(app)
    TALISMAN.init_app(app, content_security_policy=CSP, force_https=False)

    return app


def init_logs(app):
    """Функция для инициализации логов для приложения"""
    logs = create_logger(app)

    formatter = Formatter("%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s",
                          "%Y-%m-%d %H:%M:%S")
    debug_handler = RotatingFileHandler(f'{dirname(__file__)}/logs/debug.log',
                                        maxBytes=100000,
                                        backupCount=5)
    debug_handler.setLevel(DEBUG)
    debug_handler.setFormatter(formatter)
    logs.addHandler(debug_handler)

    error_handler = RotatingFileHandler(f'{dirname(__file__)}/logs/error.log',
                                        maxBytes=100000,
                                        backupCount=5)
    error_handler.setLevel(ERROR)
    error_handler.setFormatter(formatter)
    logs.addHandler(error_handler)


@babel.localeselector
def get_locale():
    """Функция для получения подходящей локали для приложения"""
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])
