"""Тесты для GET запросов"""
from tests import BaseTestCase


class GetQueriesTestCase(BaseTestCase):
    """Класс для тест-кейсов GET запросов"""

    def test_main_page_get_query(self):
        """Тест GET запроса для главной страницы"""
        r = self.client.get('/')
        self.assertEqual(r.status_code, 200)
        self.assertTrue('<title>Кулинарная книга</title>' in r.get_data(as_text=True))

    def test_about_query(self):
        """Тест GET запроса для странички 'О блюде'"""
        r = self.client.get('/about')
        self.assertEqual(r.status_code, 200)
        self.assertTrue('<title>О проекте</title>' in r.get_data(as_text=True))

    def test_get_dishes_query(self):
        """Тест GET запроса для странички с блюдами определенного типа"""
        r = self.client.get('/dishes/sweet_food_and_drinks')
        self.assertEqual(r.status_code, 200)
        self.assertTrue('<title>Сладкие блюда и напитки</title>' in r.get_data(as_text=True))

    def test_search_dishes_query(self):
        """Тест GET запроса для поиска блюд определенного типа"""
        r = self.client.get('/dishes/sweet_food_and_drinks?dish_name=к')
        self.assertEqual(r.status_code, 200)
        self.assertTrue('<title>Сладкие блюда и напитки</title>' in r.get_data(as_text=True))

        r = self.client.get('/dishes/sweet_food_and_drinks?dish_name=мандарин')
        self.assertEqual(r.status_code, 200)
        self.assertTrue('<title>Сладкие блюда и напитки</title>' in r.get_data(as_text=True))

        r = self.client.get('/dishes/sweet_food_and_drinks?dish_name=мандарины')
        self.assertEqual(r.status_code, 200)
        self.assertTrue('<title>Сладкие блюда и напитки</title>' in r.get_data(as_text=True))

    def test_get_service_worker(self):
        """Тест GET запроса для получения sw.js (service worker)"""
        r = self.client.get('/static/js/sw.js')
        self.assertEqual(r.headers.get('Content-Type'), 'application/javascript; charset=utf-8')
        self.assertEqual(r.status_code, 200)

    def test_get_robots_txt_file(self):
        """Тест GET запроса для получения файла robots.txt"""
        r = self.client.get('/static/robots.txt')
        self.assertEqual(r.headers.get('Content-Type'), 'text/plain; charset=utf-8')
        self.assertEqual(r.status_code, 200)
