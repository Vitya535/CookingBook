"""Тесты для SQL запросов"""
from test import BaseTestCase
from app.orm_db_actions import delete_dish
from app.orm_db_actions import search_dishes
from app.utils import TypesOfDish


class SQLQueriesTestCase(BaseTestCase):
    """Класс для тест-кейсов SQL запросов через ORM"""

    def test_get_dishes_by_type(self):
        """Тест SQL запроса на получение определенного типа блюд"""
        self.check_get_dishes_by_type()

    def test_get_dishes_by_type_and_name(self):
        """Тест SQL запроса на получение определенного типа блюд, совпадающих с вхождением названия"""
        with self.app.test_request_context():
            expected = list(self.dishes[1:3])
            result = search_dishes(TypesOfDish.SWEET_FOOD_AND_DRINKS, 'к')
            self.assertEqual(expected, result)

            expected = [self.dishes[2]]
            result = search_dishes(TypesOfDish.SWEET_FOOD_AND_DRINKS, 'рождественский')
            self.assertEqual(expected, result)

            expected = []
            result = search_dishes(TypesOfDish.SWEET_FOOD_AND_DRINKS, 'hello')
            self.assertEqual(expected, result)

    def test_delete_dish_by_name(self):
        """Тест SQL запроса на удаление блюда по его полному названию"""
        with self.app.test_request_context():
            delete_dish('Кекс рождественский с мандаринами')
            result = search_dishes(TypesOfDish.SWEET_FOOD_AND_DRINKS, 'Кекс рождественский с мандаринами')
            self.assertEqual(result, [])
