"""Файл, реализующий формы для страничек"""
from flask_babel import lazy_gettext
from markupsafe import Markup
from wtforms import Form
from wtforms import StringField
from wtforms.validators import DataRequired
from wtforms.validators import Length
from wtforms.widgets import html_params


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
    """Форма для поиска блюд по его названию"""
    dish_name = StringField(lazy_gettext('Название блюда'),
                            [DataRequired(),
                             Length(min=1, max=50)],
                            render_kw={'class': 'form-control', 'placeholder': lazy_gettext('Название блюда')})
    button_search = ButtonField('<svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-search" '
                                'fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" '
                                'd="M10.442 10.442a1 1 0 0 1 1.415 0l3.85 3.85a1 1 0 0 1-1.414 1.415l-3.85-3.85a1 1 '
                                '0 0 1 0-1.415z"/>'
                                '<path fill-rule="evenodd" d="M6.5 12a5.5 5.5 0 1 0 0-11 5.5 5.5 0 0 0 0 11zM13 6.5a6.5'
                                ' 6.5 0 1 1-13 0 6.5 6.5 0 0 1 13 0z"/></svg>',
                                render_kw={'title': lazy_gettext('Поиск'), 'class': 'btn btn-success'})
