"""Тесты для POST запросов"""
from app.orm_db_actions import search_dishes
from app.utils import TypesOfDish
from test import BaseTestCase


class PostQueriesTestCase(BaseTestCase):
    """Класс для тест-кейсов POST запросов"""

    def test_delete_query(self):
        """Тест POST запроса удаления блюда"""
        with self.app.test_request_context() as ctx:
            self.app.config['WTF_CSRF_ENABLED'] = False
            dish_name = 'Печенье Мордашки'
            r = self.client.post('/delete', data={'dish_name': dish_name})
            result = search_dishes(TypesOfDish.SWEET_FOOD_AND_DRINKS, dish_name)
            self.assertEqual(r.get_data(as_text=True), '{}\n')
            self.assertEqual(result, [])
            self.assertEqual(r.status_code, 200)
