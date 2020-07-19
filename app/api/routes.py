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
    if not dishes_dict:
        abort(404)
    return jsonify(dishes_dict)


@bp.route('/dishes/<int:dish_id>')
def get_dish(dish_id: int):
    """GET запрос, достающий блюдо по его id, если оно есть в базе"""
    return jsonify(Dish.query.get_or_404(dish_id).to_dict())


@bp.route('/dishes', methods=['POST'])
def create_dish():
    """POST запрос, создающий блюдо по JSON, который приходит на вход"""
    data = request.get_json() or {}
    if 'name' not in data or 'description' not in data or 'portion_count' not in data or 'type_of_dish' not in data:
        abort(400)
    if Dish.query.filter_by(name=data['name']).first():
        abort(400)
    if Dish.query.filter_by(description=data['description']).first():
        abort(400)
    new_dish = Dish(data['description'], data['name'], data['portion_count'], data['type_of_dish'])
    db.session.add(new_dish)
    db.session.commit()
    return jsonify(new_dish.to_dict()), 201



@bp.route('/dishes/<int:dish_id>', methods=['PUT'])
def update_dish(dish_id: int):
    """PUT запрос, редактирующий данные о блюде по JSON, который приходит на вход"""
    dish = Dish.query.get_or_404(dish_id)
    data = request.get_json() or {}
    if 'name' not in data or 'description' not in data or 'portion_count' not in data or 'type_of_dish' not in data:
        abort(400)
    if Dish.query.filter_by(name=data['name']).first():
        abort(400)
    if Dish.query.filter_by(description=data['description']).first():
        abort(400)
    dish.description = data['description']
    dish.name = data['name']
    dish.portion_count = data['portion_count']
    dish.type_of_dish = data['type_of_dish']
    db.session.commit()
    return jsonify(dish.to_dict())


@bp.route('/dishes/<int:dish_id>', methods=['DELETE'])
def delete_dish(dish_id: int):
    """DELETE запрос, удаляющий данные о блюде с id, который приходит на вход"""
    dish = Dish.query.get_or_404(dish_id)
    db.session.delete(dish)
    db.session.commit()
    return f"Dish with id={dish_id} is deleted", 200
