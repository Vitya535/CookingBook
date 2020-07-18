"""Инициализация данных, необходимых для тестирования приложения"""
from unittest import TestCase

from app import create_app
from app.extensions import db
from app.orm_db import Dish
from app.orm_db import Implement
from app.orm_db import Ingredient
from app.orm_db import Recipe
from app.orm_db import StepOfCook
from app.utils import TypesOfDish
from app.utils import UnitsOfMeasurement


class BaseTestCase(TestCase):
    """Базовый класс для всех тест-кейсов приложения"""

    def setUp(self):
        """Инициализация необходимых параметров"""
        self.app = create_app()
        self.app_ctx = self.app.app_context()
        self.app_ctx.push()
        self.client = self.app.test_client(use_cookies=True)
        self.db = db
        self.db.create_all()
        self.populate_db()

    def tearDown(self):
        """Очистка параметров после каждого теста"""
        self.db.session.remove()
        self.db.drop_all()
        self.app_ctx.pop()

    def populate_db(self):
        """Метод для наполнения тестовой базы данных"""
        self.dishes = (Dish("Беспроигрышный вариант накормить гостей за праздничным столом - запечь курицу целиком в духовке. Блюдо смотрится богато и аппетитно! Птицу замаринуйте в соевом маринаде, затем смажьте творожным сыром.", "Курица с сыром в духовке (Жар птица)", 6, TypesOfDish.MEAT_DISHES),
                       Dish("На новогодние праздники не забудьте удивить своих маленьких непосед. Забавное печенье обязательно им понравится. Печенье в виде мордашки собаки легко испечь вместе с детьми, без специальной формочки.", "Печенье Мордашки", 8, TypesOfDish.SWEET_FOOD_AND_DRINKS),
                       Dish("Рождественский кекс – это обязательное блюдо на Рождество на западе. Эта традиция дошла и до нас. Кекс получается невероятно вкусным благодаря цитрусам, специям и рождественскому волшебству.", "Кекс рождественский с мандаринами", 7, TypesOfDish.SWEET_FOOD_AND_DRINKS))
        self.recipes = (Recipe("/static/img/kurica_s_sirom_v_duhovke.webp", "https://povar.ru/recipes/kurica_s_syrom_v_duhovke_jar_ptica-72195.html", "30 мин.", "2 ч.", 1),
                        Recipe("/static/img/pechenie_mordashki.webp", "https://povar.ru/recipes/pechene_mordashki-65369.html", "30 мин.", "1 ч. 30 мин", 2),
                        Recipe("/static/img/keks_rojdestvenskii_s_mandarinami.webp", "https://povar.ru/recipes/keks_rojdestvenskii_s_mandarinami-52483.html", "30 мин.", "2 ч.", 3))
        self.implements = (Implement("Бумажные полотенца"),
                           Implement("Противень"),
                           Implement("Пергамент для выпечки"),
                           Implement("Деревянные шпажки"),
                           Implement("Измельчитель"),
                           Implement("Духовка"),
                           Implement("Миксер"))
        self.steps_of_cook = (StepOfCook(1, "Выпотрошенную тушку курицы промойте под холодной водой, обсушите бумажными полотенцами. Соедините соевый соус, горчицу и растительное масло. Натрите смесью птицу внутри и снаружи. Оставьте мариноваться на 20 минут.", 1),
                              StepOfCook(2, "Курицу разрежьте по грудке и разверните, как на фото. Натрите сушенным чесноком. Поместите курицу на противень с пергаментом для выпечки.", 1),
                              StepOfCook(3, "Смажьте верх птицы творожным сыром с зеленым луком. Поставьте запекаться в разогретую до 200 градусов духовку на 30 минут. Уменьшите температуру до 180 градусов и продолжайте запекать курицу до готовности. Время готовки зависит от веса курицы. У меня заняло 1,5 часа.", 1),
                              StepOfCook(4, "Проверьте курицу на готовность: проткните мясо деревянной шпажкой, выделившийся сок должен быть прозрачным.", 1),
                              StepOfCook(5, "Подавайте 'Жар птицу' с отварным рисом, свежей зеленью и овощами. Приятного аппетита!", 1),
                              StepOfCook(1, "Подготовьте необходимые продукты. Для белого теста: 150 г муки, 100 г сливочного масла, 50 г сахара.", 2),
                              StepOfCook(2, "Для шоколадного теста: 130 г муки, какао - 1 ст. л., 100 г сливочного масла, 50 г сахара.", 2),
                              StepOfCook(3, "Сахар и масло взбейте в измельчителе до однородной массы, добавьте просеянную муку, перемешивайте только тех пор, пока тесто не начнет собираться в комок. Также замесите шоколадное тесто. Накройте пищевой пленкой и оставьте в холодильнике на 1 час.", 2),
                              StepOfCook(4, "Белое тесто разделите на 16 равных частей. Скатайте жгутики и сверните их спиралью.", 2),
                              StepOfCook(5, "Шоколадное тесто раскатайте в пласт, толщиной 5 мм. Вырубите кружки для мордочек, глаз и носиков (по желанию их можно заменить на шоколадные капли). Ушки-треугольники прилепите к мордочкам и загните. Зубочисткой нарисуйте рот на кружке мордочки. Еще один вариант печенья-мордочек можно сделать с помощью вырубки 'сердце'. Белое сердце - мордочка, шоколадное пополам - ушки.", 2),
                              StepOfCook(6, "Выпекайте печенье-мордашки в разогретой до 200 °С духовке в течение 15 минут. Остудите полностью. Приятного аппетита! Счастливого Нового года!", 2),
                              StepOfCook(1, "Очистите мандарины, выложите дольки на 1 час, чтобы пленочка немного подсохла.", 3),
                              StepOfCook(2, "Сухофрукты залейте апельсиновым ликером на 30 минут.", 3),
                              StepOfCook(3, "Размягченное сливочное масло взбейте с сахаром в пышную массу с помощью миксера.", 3),
                              StepOfCook(4, "Далее по одному вбивайте яйца, не останавливая работу миксера.", 3),
                              StepOfCook(5, "Просейте муку вместе с разрыхлителем и аккуратно взбивайте на небольшой скорости.", 3),
                              StepOfCook(6, "На разогретую сковороду выложите 20 грамм сливочного масла. Добавьте 1 ч.ложку сахара, а затем выложите дольки мандарина и обжаривайте с каждой стороны по 2 минуты.", 3),
                              StepOfCook(7, "На эту же сковороду отправьте сухофрукты в ликере. Прогревайте, пока не испарится алкоголь. Когда они остынут - отправьте их в тесто и аккуратно перемешайте.", 3),
                              StepOfCook(8, "Форму для выпечки смажьте маслом и присыпьте мукой. Выложите тесто, перекладывая его карамелизированными мандаринами. Выпекайте 1 час в духовке, разогретой до 180 градусов.", 3),
                              StepOfCook(9, "Когда кекс остынет, украсьте его взбитым белком, присыпьте сахарной пудрой. Выложите дольки мандарина и лимонную цедру. Розмарин заменит елочные ветки.", 3))
        self.ingredients = (Ingredient("Курица", 3, UnitsOfMeasurement.KILOGRAM),
                            Ingredient("Соевый соус", 2, UnitsOfMeasurement.TABLE_SPOON),
                            Ingredient("Горчица", 2, UnitsOfMeasurement.TABLE_SPOON),
                            Ingredient("Масло растительное", 2, UnitsOfMeasurement.TABLE_SPOON),
                            Ingredient("Чеснок сушеный", 1, UnitsOfMeasurement.TABLE_SPOON),
                            Ingredient("Сыр творожный", 150, UnitsOfMeasurement.GRAM),
                            Ingredient("Мука", 280, UnitsOfMeasurement.GRAM),
                            Ingredient("Масло сливочное", 200, UnitsOfMeasurement.GRAM),
                            Ingredient("Сахар", 100, UnitsOfMeasurement.GRAM),
                            Ingredient("Какао-порошок", 1, UnitsOfMeasurement.TABLE_SPOON),
                            Ingredient("Шоколадные капли", 10, UnitsOfMeasurement.GRAM),
                            Ingredient("Сливочное масло", 150, UnitsOfMeasurement.GRAM),
                            Ingredient("Сахар", 125, UnitsOfMeasurement.GRAM),
                            Ingredient("Мука", 125, UnitsOfMeasurement.GRAM),
                            Ingredient("Яйца", 3, UnitsOfMeasurement.SHTUKI),
                            Ingredient("Разрыхлитель", 1, UnitsOfMeasurement.TEA_SPOON),
                            Ingredient("Мандарины", 2, UnitsOfMeasurement.SHTUKI),
                            Ingredient("Сухофрукты", 150, UnitsOfMeasurement.GRAM),
                            Ingredient("Апельсиновый ликер", 2, UnitsOfMeasurement.TABLE_SPOON),
                            Ingredient("Сливочное масло", 20, UnitsOfMeasurement.GRAM),
                            Ingredient("Сахар", 1, UnitsOfMeasurement.TEA_SPOON),
                            Ingredient("Мелкий сахар", 1, UnitsOfMeasurement.TABLE_SPOON),
                            Ingredient("Яичный белок", 1, UnitsOfMeasurement.SHTUKI),
                            Ingredient("Мандарины", 1, UnitsOfMeasurement.SHTUKI),
                            Ingredient("Лимон", 1, UnitsOfMeasurement.SHTUKI),
                            Ingredient("Веточка розмарина", 1, UnitsOfMeasurement.SHTUKI),
                            Ingredient("Сахарная пудра", 1, UnitsOfMeasurement.TABLE_SPOON))
        for dish in self.dishes:
            self.db.session.add(dish)
            self.db.session.commit()
        for recipe in self.recipes:
            self.db.session.add(recipe)
            self.db.session.commit()
        for implement in self.implements:
            self.db.session.add(implement)
            self.db.session.commit()
        for step_of_cook in self.steps_of_cook:
            self.db.session.add(step_of_cook)
            self.db.session.commit()
        for ingredient in self.ingredients:
            self.db.session.add(ingredient)
            self.db.session.commit()
