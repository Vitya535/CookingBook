"""Файл с тест-кейсами для API в приложении"""
from test import BaseTestCase


class ApiTestCase(BaseTestCase):
    """Класс тест-кейса для тестирования API к приложению"""

    def assert_response(self, r, status_code, content_type, json_data):
        """Проверка ответа"""
        self.assertEqual(r.status_code, status_code)
        self.assertEqual(r.headers['Content-Type'], content_type)
        self.assertEqual(r.get_json(), json_data)

    def test_get_all_dishes(self):
        """Тестирование GET запроса в API для получения всех блюд"""
        r = self.client.get('/api/dishes')
        self.assert_response(r, 200, 'application/json', list(dish.to_dict() for dish in self.dishes))

    def test_get_dish_by_id(self):
        """Тестирование GET запроса в API для получения блюда по его id"""
        r = self.client.get('/api/dishes/1')
        self.assert_response(r, 200, 'application/json', self.dishes[0].to_dict())

        r = self.client.get('/api/dishes/100')
        self.assert_response(r, 404, 'application/json', {'message': 'The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.'})

    def test_create_dish(self):
        """Тестирование POST запроса в API для добавления нового блюда"""
        self.app.config['WTF_CSRF_ENABLED'] = False
        new_dish_data = {
            'description': 'Соус из запеченных баклажан и помидоров отлично сочетается с мясом, матнакашем, запеченным картофелем. Остроты добавит свежий лук. Можно дать настояться около часа, так соус-дип станет еще вкуснее.',
            'name': 'Соус-дип из запеченных баклажан',
            'portion_count': 4,
            'type_of_dish': 'Соусы и маринады'
        }
        r = self.client.post('/api/dishes', json=new_dish_data)
        new_dish_data.update({'id': 4})
        self.assert_response(r, 200, 'application/json', new_dish_data)

    def test_create_dish_without_unique_name(self):
        """Тест создания блюда через POST запрос с его неуникальным названием"""
        self.app.config['WTF_CSRF_ENABLED'] = False
        new_dish_data = {
            'description': 'Соус из запеченных баклажан и помидоров отлично сочетается с мясом, матнакашем, запеченным картофелем. Остроты добавит свежий лук. Можно дать настояться около часа, так соус-дип станет еще вкуснее.',
            'name': 'Печенье Мордашки',
            'portion_count': 4,
            'type_of_dish': 'Соусы и маринады'
        }
        r = self.client.post('/api/dishes', json=new_dish_data)
        self.assert_response(r, 400, 'application/json', {'message': 'The browser (or proxy) sent a request that this server could not understand.'})

    def test_create_dish_without_unique_description(self):
        """Тест создания блюда через POST запрос с его неуникальным описанием"""
        self.app.config['WTF_CSRF_ENABLED'] = False
        new_dish_data = {
            'description': 'Беспроигрышный вариант накормить гостей за праздничным столом - запечь курицу целиком в духовке. Блюдо смотрится богато и аппетитно! Птицу замаринуйте в соевом маринаде, затем смажьте творожным сыром.',
            'name': 'Соус-дип из запеченных баклажан',
            'portion_count': 4,
            'type_of_dish': 'Соусы и маринады'
        }
        r = self.client.post('/api/dishes', json=new_dish_data)
        self.assert_response(r, 400, 'application/json', {'message': 'The browser (or proxy) sent a request that this server could not understand.'})

    def test_create_dish_without_one_param(self):
        """Тест создания блюда через POST запрос с отсутствием одного из необходимых параметров"""
        self.app.config['WTF_CSRF_ENABLED'] = False
        new_dish_data = {
            'description': 'Соус из запеченных баклажан и помидоров отлично сочетается с мясом, матнакашем, запеченным картофелем. Остроты добавит свежий лук. Можно дать настояться около часа, так соус-дип станет еще вкуснее.',
            'name': 'Соус-дип из запеченных баклажан',
            'portion_count': 4
        }
        r = self.client.post('/api/dishes', json=new_dish_data)
        self.assert_response(r, 400, 'application/json', {'message': 'The browser (or proxy) sent a request that this server could not understand.'})

    def test_create_dish_with_enabled_csrf(self):
        """Тест создания блюда через POST запрос с включенной CSRF-защитой"""
        self.app.config['WTF_CSRF_ENABLED'] = True
        new_dish_data = {
            'description': 'Соус из запеченных баклажан и помидоров отлично сочетается с мясом, матнакашем, запеченным картофелем. Остроты добавит свежий лук. Можно дать настояться около часа, так соус-дип станет еще вкуснее.',
            'name': 'Соус-дип из запеченных баклажан',
            'portion_count': 4,
            'type_of_dish': 'Соусы и маринады'
        }
        r = self.client.post('/api/dishes', json=new_dish_data)
        self.assertTrue(r.headers.get('X-CSRFToken') is None)
        self.assert_response(r, 400, 'application/json', {'message': 'The CSRF token is missing.'})

    def test_update_dish(self):
        """Тестирование PUT запроса в API для редактирования нового блюда"""
        self.app.config['WTF_CSRF_ENABLED'] = False
        data_to_update = {
            'description': 'Соус из запеченных баклажан и помидоров отлично сочетается с мясом, матнакашем, запеченным картофелем. Остроты добавит свежий лук. Можно дать настояться около часа, так соус-дип станет еще вкуснее.',
            'name': 'Соус-дип из запеченных баклажан',
            'portion_count': 4,
            'type_of_dish': 'Соусы и маринады'
        }
        r = self.client.put('/api/dishes/1', json=data_to_update)
        data_to_update.update({'id': 1})
        self.assert_response(r, 200, 'application/json', data_to_update)

    def test_update_not_existing_dish(self):
        """Тест редактирования блюда через PUT запрос несуществующего блюда"""
        self.app.config['WTF_CSRF_ENABLED'] = False
        data_to_update = {
            'description': 'Соус из запеченных баклажан и помидоров отлично сочетается с мясом, матнакашем, запеченным картофелем. Остроты добавит свежий лук. Можно дать настояться около часа, так соус-дип станет еще вкуснее.',
            'name': 'Соус-дип из запеченных баклажан',
            'portion_count': 4,
            'type_of_dish': 'Соусы и маринады',
        }
        r = self.client.put('/api/dishes/100', json=data_to_update)
        self.assert_response(r, 404, 'application/json', {'message': 'The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.'})

    def test_update_dish_without_param(self):
        """Тест редактирования блюда через PUT запрос без одного из параметров"""
        self.app.config['WTF_CSRF_ENABLED'] = False
        data_to_update = {
            'description': 'Соус из запеченных баклажан и помидоров отлично сочетается с мясом, матнакашем, запеченным картофелем. Остроты добавит свежий лук. Можно дать настояться около часа, так соус-дип станет еще вкуснее.',
            'name': 'Соус-дип из запеченных баклажан',
            'portion_count': 4
        }
        r = self.client.put('/api/dishes/1', json=data_to_update)
        self.assert_response(r, 400, 'application/json', {'message': 'The browser (or proxy) sent a request that this server could not understand.'})

    def test_update_dish_without_unique_name(self):
        """Тест редактирования блюда через PUT запрос с его неуникальным названием"""
        self.app.config['WTF_CSRF_ENABLED'] = False
        data_to_update = {
            'description': 'Соус из запеченных баклажан и помидоров отлично сочетается с мясом, матнакашем, запеченным картофелем. Остроты добавит свежий лук. Можно дать настояться около часа, так соус-дип станет еще вкуснее.',
            'name': 'Печенье Мордашки',
            'portion_count': 4,
            'type_of_dish': 'Соусы и маринады'
        }
        r = self.client.put('/api/dishes/1', json=data_to_update)
        self.assert_response(r, 400, 'application/json', {'message': 'The browser (or proxy) sent a request that this server could not understand.'})

    def test_update_dish_without_unique_description(self):
        """Тест редактирования блюда через PUT запрос с его неуникальным описанием"""
        self.app.config['WTF_CSRF_ENABLED'] = False
        data_to_update = {
            'description': 'Беспроигрышный вариант накормить гостей за праздничным столом - запечь курицу целиком в духовке. Блюдо смотрится богато и аппетитно! Птицу замаринуйте в соевом маринаде, затем смажьте творожным сыром.',
            'name': 'Соус-дип из запеченных баклажан',
            'portion_count': 4,
            'type_of_dish': 'Соусы и маринады'
        }
        r = self.client.put('/api/dishes/1', json=data_to_update)
        self.assert_response(r, 400, 'application/json', {'message': 'The browser (or proxy) sent a request that this server could not understand.'})

    def test_update_dish_with_enabled_csrf(self):
        """Тест редактирования блюда через PUT запрос с включенной CSRF-защитой"""
        self.app.config['WTF_CSRF_ENABLED'] = True
        data_to_update = {
            'description': 'Беспроигрышный вариант накормить гостей за праздничным столом - запечь курицу целиком в духовке. Блюдо смотрится богато и аппетитно! Птицу замаринуйте в соевом маринаде, затем смажьте творожным сыром.',
            'name': 'Соус-дип из запеченных баклажан',
            'portion_count': 4,
            'type_of_dish': 'Соусы и маринады'
        }
        r = self.client.put('/api/dishes/1', json=data_to_update)
        self.assertTrue(r.headers.get('X-CSRFToken') is None)
        self.assert_response(r, 400, 'application/json', {'message': 'The CSRF token is missing.'})

    def test_delete_dish(self):
        """Тестирование DELETE запроса в API для удаления существующего блюда"""
        self.app.config['WTF_CSRF_ENABLED'] = False
        r = self.client.delete('/api/dishes/1')
        self.assert_response(r, 200, 'application/json', 'Dish with id=1 is deleted')

    def test_delete_not_existing_dish(self):
        """Тест удаления несуществующего блюда"""
        self.app.config['WTF_CSRF_ENABLED'] = False
        r = self.client.delete('/api/dishes/100')
        self.assert_response(r, 404, 'application/json', {'message': 'The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.'})

    def test_delete_dish_with_enabled_csrf(self):
        """Тест удаления блюда с включенной CSRF-защитой"""
        self.app.config['WTF_CSRF_ENABLED'] = True
        r = self.client.delete('/api/dishes/1')
        self.assertTrue(r.headers.get('X-CSRFToken') is None)
        self.assert_response(r, 400, 'application/json', {'message': 'The CSRF token is missing.'})
