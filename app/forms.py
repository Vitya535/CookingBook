"""Файл, реализующий формы для страничек"""
from flask_babel import lazy_gettext
from markupsafe import Markup
from wtforms import BooleanField
from wtforms import Form
from wtforms import PasswordField
from wtforms import StringField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired
from wtforms.validators import Length
from wtforms.widgets import html_params

from app.constants import DISH_NAME
from app.constants import EMAIL
from app.constants import ENTER
from app.constants import PASSWORD
from app.constants import REGISTRATION
from app.constants import REPEAT_PASSWORD
from app.constants import SEARCH
from app.constants import USERNAME


class ButtonWidget:
    """Класс, реализующий кнопку типа <button {params}>{label}</button>"""
    html_params = staticmethod(html_params)

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        if 'value' not in kwargs:
            kwargs['value'] = field._value()

        return Markup(f'<button {self.html_params(**kwargs)}>{field.label.text}</button>')


class ButtonField(StringField):
    """Класс, создающий из кнопки поле"""
    widget = ButtonWidget()


class DishSearchForm(Form):
    """Форма для поиска блюд по его названию"""
    dish_name = StringField(lazy_gettext(DISH_NAME),
                            [DataRequired(),
                             Length(min=1, max=50)],
                            render_kw={'class': 'form-control', 'placeholder': lazy_gettext(DISH_NAME)})
    button_search = ButtonField('<svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-search" '
                                'fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" '
                                'd="M10.442 10.442a1 1 0 0 1 1.415 0l3.85 3.85a1 1 0 0 1-1.414 1.415l-3.85-3.85a1 1 '
                                '0 0 1 0-1.415z"/>'
                                '<path fill-rule="evenodd" d="M6.5 12a5.5 5.5 0 1 0 0-11 5.5 5.5 0 0 0 0 11zM13 6.5a6.5'
                                ' 6.5 0 1 1-13 0 6.5 6.5 0 0 1 13 0z"/></svg>',
                                render_kw={'title': lazy_gettext(SEARCH), 'class': 'btn btn-success'})


class LoginForm(Form):
    """Форма для авторизации пользователя в системе"""
    email = EmailField(lazy_gettext(EMAIL), [DataRequired(), Length(min=1, max=50)],
                       render_kw={'placeholder': lazy_gettext(EMAIL), 'autofocus': '',
                                  'class': 'form-control'})
    password = PasswordField(lazy_gettext(PASSWORD), [DataRequired(), Length(min=1, max=20)],
                             render_kw={'placeholder': lazy_gettext(PASSWORD), 'class': 'form-control mb-3'})
    remember_me = BooleanField()
    submit_button = ButtonField(lazy_gettext(ENTER),
                                render_kw={'class': 'btn btn-lg btn-primary btn-block', 'type': 'submit'})


class RegistrationForm(Form):
    """Форма для регистрации пользователя в системе"""
    nickname = StringField(lazy_gettext(USERNAME), [DataRequired(), Length(min=1, max=20)],
                           render_kw={'placeholder': lazy_gettext(USERNAME), 'autofocus': '',
                                      'class': 'form-control'})
    email = EmailField(lazy_gettext(EMAIL), [DataRequired(), Length(min=1, max=50)],
                       render_kw={'placeholder': lazy_gettext(EMAIL),
                                  'class': 'form-control'})
    password = PasswordField(lazy_gettext(PASSWORD), [DataRequired(), Length(min=1, max=20)],
                             render_kw={'placeholder': lazy_gettext(PASSWORD), 'class': 'form-control'})
    repeat_password = PasswordField(lazy_gettext(REPEAT_PASSWORD), [DataRequired(), Length(min=1, max=20)],
                                    render_kw={'placeholder': lazy_gettext(REPEAT_PASSWORD),
                                               'class': 'form-control mb-3'})
    submit_button = ButtonField(lazy_gettext(REGISTRATION),
                                render_kw={'class': 'btn btn-lg btn-primary btn-block', 'type': 'submit'})
