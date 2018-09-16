"""Модуль для перечислений типов блюд и единиц измерения"""
from enum import Enum


class TypesOfDish(Enum):
    """Перечисление для типов блюд"""
    SALADS_AND_APPETIZERS = 'Салаты и закуски'
    SANDWICHES = 'Бутерброды и сэндвичи'
    MEAT_DISHES = 'Блюда из мяса'
    FISH_AND_SEAFOOD = 'Рыба и морепродукты'
    SAUCES_AND_MARINADES = 'Соусы и маринады'
    VEGETABLE_DISHES = 'Блюда из овощей'
    MILK_DISHES = 'Молочные блюда'
    CEREALS_AND_PASTA = 'Крупы и макароны'
    CAKES_AND_PASTRIES = 'Торты и выпечка'
    FRUIT_DISHES = 'Блюда из фруктов'
    LEAN_DISHES = 'Постные блюда'
    SWEET_FOOD_AND_DRINKS = 'Сладкие блюда и напитки'


class UnitsOfMeasurement(Enum):  # добавить еще единиц измерения (потом)
    """Перечисление для единиц измерения"""
    GRAM = 'грамм'
    TABLE_SPOON = 'столовые ложки'
    LITERS = 'литры'
