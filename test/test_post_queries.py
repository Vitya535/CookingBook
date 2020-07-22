"""Тесты для POST запросов"""
from test import BaseTestCase


class PostQueriesTestCase(BaseTestCase):
    """Класс для тест-кейсов POST запросов"""

    def test_delete_query(self):
        """Тест POST запроса удаления блюда"""
        with self.app.test_request_context():
            self.app.config['WTF_CSRF_ENABLED'] = False
            dish_name = 'Печенье Мордашки'
            self.check_delete_query(dish_name)
