from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import assets

APP = Flask(__name__)
APP.config.from_pyfile('config.py')

db = SQLAlchemy(APP)

from server import *

if __name__ == '__main__':
    APP.run()
