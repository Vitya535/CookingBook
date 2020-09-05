"""Файл с запросами к БД"""
from flask import current_app
from flask_babel import force_locale
from flask_babel import gettext
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.extensions import login_manager
from app.orm_db import Dish
from app.orm_db import User


def delete_dish(dish_name: str) -> None:
    """Удаление информации о блюде из БД по его названию"""
    try:
        current_app.logger.debug(f'Enter into {delete_dish.__name__} with params: dish_name={dish_name}')
        with force_locale('ru'):
            db.session.query(Dish).filter_by(name=gettext(dish_name)).delete()
        db.session.flush()
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        current_app.logger.error(f'Откат операции удаления блюда: {e}')


def search_dishes(dish_type, query_title: str) -> tuple:
    """Поиск блюд по различным параметрам"""
    current_app.logger.debug(f'Enter into {search_dishes.__name__} with params: dish_type={dish_type}, '
                             f'query_title={query_title}')
    dishes = db.session.query(Dish).filter(Dish.type_of_dish == dish_type).all()
    dishes = tuple(filter(lambda d: query_title in gettext(d.name), dishes))
    current_app.logger.debug(f'Founded dishes: {dishes}')
    return dishes


def get_user(email: str = "", nickname: str = ""):
    """Получить текущего пользователя"""
    current_app.logger.debug(f'Enter into {get_user.__name__} with params: nickname={nickname}, email={email}')
    user = db.session.query(User).filter(and_(
        User.email.like(f"%{email}%"),
        User.nickname.like(f"%{nickname}%")
    )).first()
    current_app.logger.debug(f'Founded user: {user}')
    return user


def add_user(nickname: str, email: str, password: str):
    """Добавление нового пользователя"""
    try:
        current_app.logger.debug(f'Enter into {add_user.__name__} with params: nickname={nickname}, email={email},'
                                 f' password={password}')
        user = User(nickname, email, password)
        current_app.logger.debug(f'Founded user: {user}')
        db.session.add(user)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        current_app.logger.error(f'Откат операции добавления блюда: {e}')


@login_manager.user_loader
def load_user(user_id):
    """Функция для загрузки пользователя при аутентификации/авторизации"""
    return User.query.get(int(user_id))
