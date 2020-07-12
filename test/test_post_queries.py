"""Тесты для POST запросов"""
from app.orm_db_actions import search_dishes
from app.utils import TypesOfDish
from test import BaseTestCase


class PostQueriesTestCase(BaseTestCase):
    """Класс для тест-кейсов POST запросов"""

    def test_delete_query(self):
        """Тест POST запроса удаления блюда"""
        self.app.config['WTF_CSRF_ENABLED'] = False
        dish_name = 'Печенье Мордашки'
        r = self.client.post('/delete', data=dict(dish_name=dish_name))
        result = search_dishes(TypesOfDish.SWEET_FOOD_AND_DRINKS, 'Печенье Мордашки')
        self.assertEqual('{}\n', r.get_data(as_text=True))
        self.assertEqual(result, [])
        self.assertEqual(r.status_code, 200)
