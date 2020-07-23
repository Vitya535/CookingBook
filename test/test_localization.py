"""Тесты для локализации в приложении"""
from app.orm_db_actions import delete_dish
from app.orm_db_actions import search_dishes
from app.utils import TypesOfDish
from test import BaseTestCase


class LocalizationTestCase(BaseTestCase):
    """Класс для тест-кейсов локализации в приложении"""

    app = None

    @classmethod
    def setUpClass(cls):
        """Инициализация необходимых параметров для проверки локализации"""
        super(LocalizationTestCase, cls).setUpClass()
        cls.app.config['BABEL_DEFAULT_LOCALE'] = 'en'

    def test_localization_main_page_get_query(self):
        """Тест GET запроса для главной страницы с локализацией"""
        r = self.client.get('/')
        self.assertEqual(r.status_code, 200)
        self.assertTrue('<title>Cooking book</title>' in r.get_data(as_text=True))

    def test_localization_about_query(self):
        """Тест GET запроса для странички 'О блюде' с локализацией"""
        r = self.client.get('/about')
        self.assertEqual(r.status_code, 200)
        self.assertTrue('<title>About project</title>' in r.get_data(as_text=True))

    def test_localization_get_dishes_query(self):
        """Тест GET запроса для странички с блюдами определенного типа с локализацией"""
        r = self.client.get('/dishes/sweet_food_and_drinks')
        self.assertEqual(r.status_code, 200)
        self.assertTrue('<title>Sweet food and drinks</title>' in r.get_data(as_text=True))

    def test_localization_search_dishes_query(self):
        """Тест GET запроса для поиска блюд определенного типа с локализацией"""
        r = self.client.get('/dishes/sweet_food_and_drinks?dish_name=C')
        self.assertEqual(r.status_code, 200)
        self.assertTrue('<title>Sweet food and drinks</title>' in r.get_data(as_text=True))

        r = self.client.get('/dishes/sweet_food_and_drinks?dish_name=tangerin')
        self.assertEqual(r.status_code, 200)
        self.assertTrue('<title>Sweet food and drinks</title>' in r.get_data(as_text=True))

        r = self.client.get('/dishes/sweet_food_and_drinks?dish_name=tangerines')
        self.assertEqual(r.status_code, 200)
        self.assertTrue('<title>Sweet food and drinks</title>' in r.get_data(as_text=True))

    def test_localization_not_found_error(self):
        """Тест Not Found ошибки при локализации"""
        r = self.client.get('/ab')
        self.assertEqual(r.status_code, 404)
        self.assertTrue('<title>404 Not Found Error</title>' in r.get_data(as_text=True))
        self.assertTrue('<h1>Sorry, you entered url for our cooking book site incorrectly</h1>'
                        in r.get_data(as_text=True))

    def test_localization_csrf_error(self):
        """Тест выдачи CSRF ошибки для локализации"""
        with self.app.test_request_context():
            dish_name = 'Christmas cupcake with tangerines'
            r = self.client.post('/delete', data={'dish_name': dish_name})
            result = search_dishes(TypesOfDish.SWEET_FOOD_AND_DRINKS, dish_name)
            expected = [self.dishes[2]]
            self.assertEqual(result, expected)
            self.assertTrue(r.headers.get('X-CSRFToken') is None)
            self.assertEqual(r.status_code, 400)
            self.assertTrue('<title>Csrf Error</title>' in r.get_data(as_text=True))
            self.assertTrue(
                "<h1>Sorry, on our page arise CSRF error. Sorry for inconvenience.</h1>" in r.get_data(as_text=True))

    def test_localization_delete_query(self):
        """Тест POST запроса удаления блюда с локализацией"""
        with self.app.test_request_context():
            self.app.config['WTF_CSRF_ENABLED'] = False
            dish_name = 'Muzzle Cookies'
            self.check_delete_query(dish_name)

    def test_localization_get_dishes_by_type(self):
        """Тест SQL запроса на получение определенного типа блюд с локализацией"""
        with self.app.test_request_context():
            result = search_dishes(TypesOfDish.SWEET_FOOD_AND_DRINKS, '')
            expected = list(self.dishes[1:3])
            self.assertEqual(expected, result)

            result = search_dishes(TypesOfDish.MEAT_DISHES, '')
            expected = [self.dishes[0]]
            self.assertEqual(expected, result)

            result = search_dishes(TypesOfDish.SAUCES_AND_MARINADES, '')
            expected = []
            self.assertEqual(expected, result)

    def test_localization_get_dishes_by_type_and_name(self):
        """Тест SQL запроса на получение определенного типа блюд, совпадающих с вхождением названия с локализацией"""
        with self.app.test_request_context():
            expected = list(self.dishes[1:3])
            result = search_dishes(TypesOfDish.SWEET_FOOD_AND_DRINKS, 'C')
            self.assertEqual(expected, result)

            expected = [self.dishes[2]]
            result = search_dishes(TypesOfDish.SWEET_FOOD_AND_DRINKS, 'Christmas')
            self.assertEqual(expected, result)

            expected = []
            result = search_dishes(TypesOfDish.SWEET_FOOD_AND_DRINKS, 'к')
            self.assertEqual(expected, result)

    def test_localization_delete_dish_by_name(self):
        """Тест SQL запроса на удаление блюда по его полному названию с локализацией"""
        with self.app.test_request_context():
            delete_dish('Christmas cupcake with tangerines')
            result = search_dishes(TypesOfDish.SWEET_FOOD_AND_DRINKS, 'Christmas cupcake with tangerines')
            self.assertEqual(result, [])
