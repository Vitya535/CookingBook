"""Файл с тест-кейсами для API в приложении"""
from test import BaseTestCase


class ApiTestCase(BaseTestCase):
    """Класс тест-кейса для тестирования API к приложению"""

    def test_get_all_dishes(self):
        """Тестирование GET запроса в API для получения всех блюд"""
        r = self.client.get('/api/dishes')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.headers['Content-Type'], 'application/json')
        self.assertEqual(r.get_json(), list(dish.to_dict() for dish in self.dishes))

    def test_get_dish_by_id(self):
        """Тестирование GET запроса в API для получения блюда по его id"""
        r = self.client.get('/api/dishes/1')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.headers['Content-Type'], 'application/json')
        self.assertEqual(r.get_json(), self.dishes[0].to_dict())

        r = self.client.get('/api/dishes/100')
        self.assertEqual(r.status_code, 404)
        self.assertEqual(r.headers['Content-Type'], 'text/html; charset=utf-8')
        self.assertEqual(r.get_json(), None)
        self.assertTrue('<title>404 Not Found Error</title>' in r.get_data(as_text=True))
        self.assertTrue('<h1>Пичалька, вы неправильно ввели URL для нашего сайта кулинарной книги</h1>'
                        in r.get_data(as_text=True))

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
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.headers['Content-Type'], 'application/json')
        self.assertEqual(r.get_json(), new_dish_data)

        new_dish_data = {
            'description': 'Соус из запеченных баклажан и помидоров отлично сочетается с мясом, матнакашем, запеченным картофелем. Остроты добавит свежий лук. Можно дать настояться около часа, так соус-дип станет еще вкуснее.',
            'name': 'Печенье Мордашки',
            'portion_count': 4,
            'type_of_dish': 'Соусы и маринады'
        }
        r = self.client.post('/api/dishes', json=new_dish_data)
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.headers['Content-Type'], 'text/html; charset=utf-8')
        self.assertEqual(r.get_json(), None)

        new_dish_data = {
            'description': 'Беспроигрышный вариант накормить гостей за праздничным столом - запечь курицу целиком в духовке. Блюдо смотрится богато и аппетитно! Птицу замаринуйте в соевом маринаде, затем смажьте творожным сыром.',
            'name': 'Соус-дип из запеченных баклажан',
            'portion_count': 4,
            'type_of_dish': 'Соусы и маринады'
        }
        r = self.client.post('/api/dishes', json=new_dish_data)
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.headers['Content-Type'], 'text/html; charset=utf-8')
        self.assertEqual(r.get_json(), None)

        new_dish_data = {
            'description': 'Соус из запеченных баклажан и помидоров отлично сочетается с мясом, матнакашем, запеченным картофелем. Остроты добавит свежий лук. Можно дать настояться около часа, так соус-дип станет еще вкуснее.',
            'name': 'Соус-дип из запеченных баклажан',
            'portion_count': 4
        }
        r = self.client.post('/api/dishes', json=new_dish_data)
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.headers['Content-Type'], 'text/html; charset=utf-8')
        self.assertEqual(r.get_json(), None)

        self.app.config['WTF_CSRF_ENABLED'] = True
        new_dish_data = {
            'description': 'Соус из запеченных баклажан и помидоров отлично сочетается с мясом, матнакашем, запеченным картофелем. Остроты добавит свежий лук. Можно дать настояться около часа, так соус-дип станет еще вкуснее.',
            'name': 'Соус-дип из запеченных баклажан',
            'portion_count': 4,
            'type_of_dish': 'Соусы и маринады'
        }
        r = self.client.post('/api/dishes', json=new_dish_data)
        self.assertTrue(r.headers.get('X-CSRFToken') is None)
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.headers['Content-Type'], 'text/html; charset=utf-8')
        self.assertTrue('<title>Csrf Error</title>' in r.get_data(as_text=True))
        self.assertTrue(
            "<h1>К сожалению, на странице произошла CSRF-ошибка. Приносим извинения за доставленные неудобства</h1>" in r.get_data(
                as_text=True))
        self.assertEqual(r.get_json(), None)

    def test_update_dish(self):
        """Тестирование PUT запроса в API для редактирования нового блюда"""
        self.app.config['WTF_CSRF_ENABLED'] = False
        data_to_update = {
            'description': 'Соус из запеченных баклажан и помидоров отлично сочетается с мясом, матнакашем, запеченным картофелем. Остроты добавит свежий лук. Можно дать настояться около часа, так соус-дип станет еще вкуснее.',
            'name': 'Соус-дип из запеченных баклажан',
            'portion_count': 4,
            'type_of_dish': 'Соусы и маринады',
        }
        r = self.client.put('/api/dishes/1', json=data_to_update)
        data_to_update.update({'id': 1})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.headers['Content-Type'], 'application/json')
        self.assertEqual(r.get_json(), data_to_update)

        r = self.client.put('/api/dishes/100', json=data_to_update)
        self.assertEqual(r.status_code, 404)
        self.assertEqual(r.headers['Content-Type'], 'text/html; charset=utf-8')
        self.assertEqual(r.get_json(), None)
        self.assertTrue('<title>404 Not Found Error</title>' in r.get_data(as_text=True))
        self.assertTrue('<h1>Пичалька, вы неправильно ввели URL для нашего сайта кулинарной книги</h1>'
                        in r.get_data(as_text=True))

        data_to_update = {
            'description': 'Соус из запеченных баклажан и помидоров отлично сочетается с мясом, матнакашем, запеченным картофелем. Остроты добавит свежий лук. Можно дать настояться около часа, так соус-дип станет еще вкуснее.',
            'name': 'Соус-дип из запеченных баклажан',
            'portion_count': 4
        }
        r = self.client.put('/api/dishes/1', json=data_to_update)
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.headers['Content-Type'], 'text/html; charset=utf-8')
        self.assertEqual(r.get_json(), None)

        data_to_update = {
            'description': 'Соус из запеченных баклажан и помидоров отлично сочетается с мясом, матнакашем, запеченным картофелем. Остроты добавит свежий лук. Можно дать настояться около часа, так соус-дип станет еще вкуснее.',
            'name': 'Печенье Мордашки',
            'portion_count': 4,
            'type_of_dish': 'Соусы и маринады'
        }
        r = self.client.put('/api/dishes/1', json=data_to_update)
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.headers['Content-Type'], 'text/html; charset=utf-8')
        self.assertEqual(r.get_json(), None)

        data_to_update = {
            'description': 'Беспроигрышный вариант накормить гостей за праздничным столом - запечь курицу целиком в духовке. Блюдо смотрится богато и аппетитно! Птицу замаринуйте в соевом маринаде, затем смажьте творожным сыром.',
            'name': 'Соус-дип из запеченных баклажан',
            'portion_count': 4,
            'type_of_dish': 'Соусы и маринады'
        }
        r = self.client.put('/api/dishes/1', json=data_to_update)
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.headers['Content-Type'], 'text/html; charset=utf-8')
        self.assertEqual(r.get_json(), None)

        self.app.config['WTF_CSRF_ENABLED'] = True
        data_to_update = {
            'description': 'Беспроигрышный вариант накормить гостей за праздничным столом - запечь курицу целиком в духовке. Блюдо смотрится богато и аппетитно! Птицу замаринуйте в соевом маринаде, затем смажьте творожным сыром.',
            'name': 'Соус-дип из запеченных баклажан',
            'portion_count': 4,
            'type_of_dish': 'Соусы и маринады'
        }
        r = self.client.put('/api/dishes/1', json=data_to_update)
        self.assertEqual(r.get_json(), None)
        self.assertTrue(r.headers.get('X-CSRFToken') is None)
        self.assertEqual(r.status_code, 400)
        self.assertTrue('<title>Csrf Error</title>' in r.get_data(as_text=True))
        self.assertTrue(
            "<h1>К сожалению, на странице произошла CSRF-ошибка. Приносим извинения за доставленные неудобства</h1>" in r.get_data(
                as_text=True))

    def test_delete_dish(self):
        """Тестирование DELETE запроса в API для удаления существующего блюда"""
        self.app.config['WTF_CSRF_ENABLED'] = False
        r = self.client.delete('/api/dishes/1')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.headers['Content-Type'], 'text/html; charset=utf-8')
        self.assertTrue(f"Dish with id=1 is deleted" in r.get_data(as_text=True))

        r = self.client.delete('/api/dishes/100')
        self.assertEqual(r.status_code, 404)
        self.assertEqual(r.headers['Content-Type'], 'text/html; charset=utf-8')
        self.assertTrue('<title>404 Not Found Error</title>' in r.get_data(as_text=True))
        self.assertTrue('<h1>Пичалька, вы неправильно ввели URL для нашего сайта кулинарной книги</h1>'
                        in r.get_data(as_text=True))

        self.app.config['WTF_CSRF_ENABLED'] = True
        r = self.client.delete('/api/dishes/1')
        self.assertTrue(r.headers.get('X-CSRFToken') is None)
        self.assertEqual(r.status_code, 400)
        self.assertTrue('<title>Csrf Error</title>' in r.get_data(as_text=True))
        self.assertTrue(
            "<h1>К сожалению, на странице произошла CSRF-ошибка. Приносим извинения за доставленные неудобства</h1>" in r.get_data(
                as_text=True))
