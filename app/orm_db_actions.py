"""Файл с запросами к БД"""
from sqlalchemy import and_

from app import DB
from app.orm_db import Dish


def delete_dish(dish_name: str) -> None:
    """Удаление информации о блюде из БД по его названию"""
    DB.session.query(Dish).filter_by(name=dish_name).delete()
    DB.session.flush()
    DB.session.commit()


def search_dishes(dish_type, query_title: str) -> list:
    """Поиск блюд по различным параметрам"""
    dishes = DB.session.query(Dish).filter(and_(Dish.name.like(f'%{query_title}%'),
                                                Dish.type_of_dish.like(dish_type))).all()
    return dishes
