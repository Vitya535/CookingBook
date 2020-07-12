"""Тесты для различных ошибок в приложении """
from app.orm_db_actions import search_dishes
from app.utils import TypesOfDish
from test import BaseTestCase


class ErrorTestCase(BaseTestCase):
    """Класс для тест-кейсов ошибок в приложении"""

    def test_not_found_error(self):
        r = self.client.get('/ab')
        self.assertEqual(r.status_code, 404)
        self.assertTrue('<title>404 Not Found Error</title>' in r.get_data(as_text=True))
        self.assertTrue('<h1>Пичалька, вы неправильно ввели URL для нашего сайта кулинарной книги</h1>'
                        in r.get_data(as_text=True))

    def test_csrf_error(self):
        dish_name = 'Кекс рождественский с мандаринами'
        r = self.client.post('/delete', data={'dish_name': dish_name})
        result = search_dishes(TypesOfDish.SWEET_FOOD_AND_DRINKS, dish_name)
        expected = [self.dishes[2]]
        self.assertEqual(result, expected)
        self.assertTrue(r.headers.get('X-CSRFToken') is None)
        self.assertEqual(r.status_code, 400)
        self.assertTrue("<h1>К сожалению, на странице произошла CSRF-ошибка. Приносим извинения за доставленные неудобства</h1>" in r.get_data(as_text=True))
