"""Инициализация маршрутов для API в приложении"""
from flask_restful import Api

from app.api.routes import AllDishesResource
from app.api.routes import DishResource

api = Api(prefix='/api')

api.add_resource(AllDishesResource, '/dishes')
api.add_resource(DishResource, '/dishes/<int:dish_id>')
