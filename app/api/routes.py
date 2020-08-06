"""Файл с маршрутами для API"""
from flask import abort
from flask import jsonify
from flask import request
from flask_restful import Resource

from app.extensions import db
from app.orm_db_actions import Dish


def check_json_data(data):
    """Проверка пришедших JSON-данных на валидность"""
    dish_attrs = ('name', 'description', 'portion_count', 'type_of_dish')
    if any((not all(attribute in data for attribute in dish_attrs),
            Dish.query.filter((Dish.name == data['name']) | (Dish.description == data['description'])).first())):
        abort(400)


class AllDishesResource(Resource):
    """Ресурс API для того, чтобы достать все блюда и создать блюдо"""

    def get(self):
        """GET запрос, достающий все блюда, которые есть в БД"""
        dishes_dict = tuple(dish.to_dict() for dish in Dish.query.all())
        return jsonify(dishes_dict)

    def post(self):
        """POST запрос, создающий блюдо по JSON, который приходит на вход"""
        data = request.get_json() or {}
        check_json_data(data)
        dish = Dish()
        dish.from_dict(data)
        db.session.add(dish)
        db.session.commit()
        return jsonify(dish.to_dict())


class DishResource(Resource):
    """Ресурс API для того, чтобы достать конкретное блюдо по id, отредактировать его или же удалить"""

    def get(self, dish_id):
        """GET запрос, достающий блюдо по его id, если оно есть в базе"""
        return jsonify(Dish.query.get_or_404(dish_id).to_dict())

    def put(self, dish_id):
        """PUT запрос, редактирующий данные о блюде по JSON, который приходит на вход"""
        dish = Dish.query.get_or_404(dish_id)
        data = request.get_json() or {}
        check_json_data(data)
        dish.from_dict(data)
        db.session.commit()
        return jsonify(dish.to_dict())

    def delete(self, dish_id):
        """DELETE запрос, удаляющий данные о блюде с id, который приходит на вход"""
        dish = Dish.query.get_or_404(dish_id)
        db.session.delete(dish)
        db.session.commit()
        return f"Dish with id={dish_id} is deleted", 200
