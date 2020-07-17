"""Файл, реализующий формы для страничек"""
from markupsafe import Markup
from wtforms import Form
from wtforms import IntegerField
from wtforms import SelectField
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import DataRequired
from wtforms.validators import Length
from wtforms.validators import NumberRange
from wtforms.widgets import html_params
from wtforms_alchemy import ModelForm
from wtforms_alchemy import Unique
from wtforms_alchemy.fields import QuerySelectMultipleField

from app.extensions import db
from app.orm_db import Dish
from app.orm_db import Implement
from app.orm_db import Ingredient
from app.orm_db import Recipe
from app.orm_db import StepOfCook
from app.utils import TypesOfDish


class ButtonWidget:
    """Класс, реализующий кнопку типа <button {params}>{label}</button>"""
    html_params = staticmethod(html_params)

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        if 'value' not in kwargs:
            kwargs['value'] = field._value()

        return Markup('<button {params}>{label}</button>'.format(
            params=self.html_params(**kwargs),
            label=field.label.text))


class ButtonField(StringField):
    """Класс, создающий из кнопки поле"""
    widget = ButtonWidget()


class DishSearchForm(Form):
    dish_name = StringField('Название блюда',
                            [DataRequired(),
                             Length(min=1, max=50)],
                            render_kw={'class': 'form-control', 'placeholder': 'Название блюда'})
    button_search = ButtonField('<svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-search" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M10.442 10.442a1 1 0 0 1 1.415 0l3.85 3.85a1 1 0 0 1-1.414 1.415l-3.85-3.85a1 1 0 0 1 0-1.415z"/><path fill-rule="evenodd" d="M6.5 12a5.5 5.5 0 1 0 0-11 5.5 5.5 0 0 0 0 11zM13 6.5a6.5 6.5 0 1 1-13 0 6.5 6.5 0 0 1 13 0z"/></svg>',
                                render_kw={'title': 'Поиск', 'class': 'btn btn-success'})


# class DishForm(ModelForm):
#     class Meta:
#         model = Dish
#
#     name = StringField('Название блюда',
#                        [DataRequired(),
#                         Unique(Dish.name,
#                                get_session=lambda: db.session,
#                                message='Такое название блюда уже существует!')])
#     description = StringField('Описание блюда',
#                               [DataRequired(),
#                                Unique(Dish.description,
#                                       get_session=lambda: db.session,
#                                       message='Такое описание блюда уже существует!')])
#     portion_count = IntegerField('Количество порций',
#                                  [DataRequired(),
#                                   NumberRange(min=1,
#                                               message='Количество порций должно быть больше нуля!')])
#     type_of_dish = SelectField('Тип блюда',
#                                choices=[('salads_and_appetizers', TypesOfDish.SALADS_AND_APPETIZERS.value),
#                                         ('sandwiches', TypesOfDish.SANDWICHES.value),
#                                         ('meat_dishes', TypesOfDish.MEAT_DISHES.value),
#                                         ('fish_and_seafood', TypesOfDish.FISH_AND_SEAFOOD.value),
#                                         ('sauces_and_marinades', TypesOfDish.SAUCES_AND_MARINADES.value),
#                                         ('vegetable_dishes', TypesOfDish.VEGETABLE_DISHES.value),
#                                         ('milk_dishes', TypesOfDish.MILK_DISHES.value),
#                                         ('cereals_and_pasta', TypesOfDish.CEREALS_AND_PASTA.value),
#                                         ('cakes_and_pastries', TypesOfDish.CAKES_AND_PASTRIES.value),
#                                         ('fruit_dishes', TypesOfDish.FRUIT_DISHES.value),
#                                         ('lean_dishes', TypesOfDish.LEAN_DISHES.value),
#                                         ('sweet_food_and_drinks', TypesOfDish.SWEET_FOOD_AND_DRINKS.value)])
#     recipes = QuerySelectMultipleField('Рецепты',
#                                        query_factory=lambda: db.session.query(Recipe).all(),
#                                        get_pk=lambda r: r.id,
#                                        get_label=lambda r: r.literature_url,
#                                        blank_text='Не указан', allow_blank=True, validators=[DataRequired()])
#     implements = QuerySelectMultipleField('Утварь',
#                                           query_factory=lambda: db.session.query(Implement).all(),
#                                           get_pk=lambda i: i.id,
#                                           get_label=lambda i: i.name,
#                                           blank_text='Не указан', allow_blank=True,
#                                           validators=[DataRequired()])
#     steps_of_cook = QuerySelectMultipleField('Шаги приготовления',
#                                              query_factory=lambda: db.session.query(StepOfCook).all(),
#                                              get_pk=lambda s: s.id,
#                                              get_label=lambda s: s.description,
#                                              blank_text='Не указан', allow_blank=True,
#                                              validators=[DataRequired()])
#     ingredients = QuerySelectMultipleField('Ингредиенты',
#                                            query_factory=lambda: db.session.query(Ingredient).all(),
#                                            get_pk=lambda i: i.id,
#                                            get_label=lambda i: i.name,
#                                            blank_text='Не указан', allow_blank=True,
#                                            validators=[DataRequired()])
#
#     button_save = SubmitField('Сохранить')
#     button_delete = SubmitField('Удалить')
