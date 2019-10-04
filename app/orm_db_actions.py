"""Файл с запросами к БД"""
from sqlalchemy import and_

from app import DB
from app.orm_db import Dish


def delete_dish(dish_name):
    """Удаление информации о блюде из БД по его имени"""
    DB.session.query(Dish).filter_by(name=dish_name).delete()
    DB.session.flush()
    DB.session.commit()


def get_dish_info(dish_type):
    """Получение блюд, соответствующих типу dish_type"""
    dishes_info = DB.session.query(Dish).filter_by(type_of_dish=dish_type).all()
    return dishes_info


def search_dishes_on_title(query_title, dish_type):
    """Поиск по названию блюда"""
    dishes = DB.session.query(Dish).filter(and_(Dish.name.like('%' + query_title + '%'),
                                                Dish.type_of_dish.like(dish_type))).all()
    return dishes

# ToDo - pylint выдает ошибки
