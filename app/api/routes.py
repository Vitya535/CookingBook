"""Файл с маршрутами для API"""
from flask import abort
from flask import jsonify
from flask import request

from app.api import bp
from app.extensions import db
from app.orm_db_actions import Dish


@bp.route('/dishes')
def get_all_dishes():
    """GET запрос, достающий все блюда, которые есть в БД"""
    dishes_dict = tuple(dish.to_dict() for dish in Dish.query.all())
    return jsonify(dishes_dict)


@bp.route('/dishes/<int:dish_id>')
def get_dish(dish_id: int):
    """GET запрос, достающий блюдо по его id, если оно есть в базе"""
    return jsonify(Dish.query.get_or_404(dish_id).to_dict())


@bp.route('/dishes', methods=['POST'])
def create_dish():
    """POST запрос, создающий блюдо по JSON, который приходит на вход"""
    data = request.get_json() or {}
    dish_attrs = ('name', 'description', 'portion_count', 'type_of_dish')
    if not all(attribute in data for attribute in dish_attrs):
        abort(400)
    if Dish.query.filter((Dish.name == data['name']) | (Dish.description == data['description'])).first():
        abort(400)
    dish = Dish()
    dish.from_dict(data)
    db.session.add(dish)
    db.session.commit()
    return jsonify(dish.to_dict()), 201


@bp.route('/dishes/<int:dish_id>', methods=['PUT'])
def update_dish(dish_id: int):
    """PUT запрос, редактирующий данные о блюде по JSON, который приходит на вход"""
    dish = Dish.query.get_or_404(dish_id)
    data = request.get_json() or {}
    dish_attrs = ('name', 'description', 'portion_count', 'type_of_dish')
    if not all(attribute in data for attribute in dish_attrs):
        abort(400)
    if Dish.query.filter((Dish.name == data['name']) | (Dish.description == data['description'])).first():
        abort(400)
    dish.from_dict(data)
    db.session.commit()
    return jsonify(dish.to_dict())


@bp.route('/dishes/<int:dish_id>', methods=['DELETE'])
def delete_dish(dish_id: int):
    """DELETE запрос, удаляющий данные о блюде с id, который приходит на вход"""
    dish = Dish.query.get_or_404(dish_id)
    db.session.delete(dish)
    db.session.commit()
    return f"Dish with id={dish_id} is deleted", 200
