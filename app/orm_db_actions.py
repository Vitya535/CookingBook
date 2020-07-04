"""Файл с запросами к БД"""
from sqlalchemy import and_

from app import DB
from app.orm_db import Dish


def delete_dish(dish_name: str) -> None:
    """Удаление информации о блюде из БД по его имени"""
    DB.session.query(Dish).filter_by(name=dish_name).delete()
    DB.session.flush()
    DB.session.commit()


def search_dishes_on_title(dish_type, query_title: str = "") -> list:
    """Поиск по названию блюда"""
    dishes = DB.session.query(Dish).filter(and_(Dish.name.like(f'%{query_title}%'),
                                                Dish.type_of_dish.like(dish_type))).all()
    return dishes
