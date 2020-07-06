"""Файл с запросами к БД"""
from flask import current_app
from sqlalchemy import and_

from app.extensions import db
from app.orm_db import Dish


def delete_dish(dish_name: str) -> None:
    """Удаление информации о блюде из БД по его названию"""
    current_app.logger.debug(f'Enter into {delete_dish.__name__} with params: dish_name={dish_name}')
    db.session.query(Dish).filter_by(name=dish_name).delete()
    db.session.flush()
    db.session.commit()


def search_dishes(dish_type, query_title: str) -> list:
    """Поиск блюд по различным параметрам"""
    current_app.logger.debug(f'Enter into {search_dishes.__name__} with params: dish_type={dish_type}, '
                             f'query_title={query_title}')
    dishes = db.session.query(Dish).filter(and_(Dish.name.like(f'%{query_title}%'),
                                                Dish.type_of_dish.like(dish_type))).all()
    current_app.logger.debug(f'Founded dishes: {dishes}')
    return dishes
