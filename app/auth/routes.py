"""Основные маршруты для JWT авторизации/аутентификации"""
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_babel import gettext
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from app.auth import bp
from app.constants import ALREADY_REGISTER
from app.constants import AUTHORIZATION
from app.constants import EMAIL
from app.constants import LOGIN
from app.constants import MESSAGE_PASSWORDS_NOT_MATCHING
from app.constants import MESSAGE_PASSWORD_IS_INCORRECT
from app.constants import MESSAGE_USERNAME_ALREADY_TAKEN
from app.constants import MESSAGE_USER_NOT_EXIST
from app.constants import PASSWORD
from app.constants import REGISTRATION
from app.constants import REPEAT_PASSWORD
from app.constants import USERNAME
from app.constants import YOU_ALREADY_REGISTER
from app.forms import LoginForm
from app.forms import RegistrationForm
from app.orm_db_actions import add_user
from app.orm_db_actions import get_user


@bp.route('/registration', methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('main.show_first_page'))
    registration_form = RegistrationForm(request.form)

    if request.method == 'POST' and registration_form.validate():
        nickname = registration_form.nickname.data
        email = registration_form.email.data
        password = registration_form.password.data
        repeat_password = registration_form.repeat_password.data

        if password != repeat_password:
            flash(gettext(MESSAGE_PASSWORDS_NOT_MATCHING))
            return render_template('auth/registration.html', form=registration_form)

        user = get_user(email, nickname)

        if user:
            flash(gettext(MESSAGE_USERNAME_ALREADY_TAKEN))
            return render_template('auth/registration.html', form=registration_form)
        else:
            add_user(nickname, email, generate_password_hash(password))
            return redirect(url_for('main.show_first_page'))

    return render_template('auth/registration.html', form=registration_form,
                           REPEAT_PASSWORD=REPEAT_PASSWORD,
                           PASSWORD=PASSWORD,
                           EMAIL=EMAIL,
                           AUTHORIZATION=AUTHORIZATION,
                           ALREADY_REGISTER=ALREADY_REGISTER,
                           REGISTRATION=REGISTRATION,
                           USERNAME=USERNAME)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.show_first_page'))
    login_form = LoginForm(request.form)

    if request.method == 'POST' and login_form.validate():
        email = login_form.email.data
        password = login_form.password.data
        remember_me = login_form.remember_me.data

        user = get_user(email)

        if not user:
            flash(gettext(MESSAGE_USER_NOT_EXIST))
            return render_template('auth/login.html', form=login_form)
        elif check_password_hash(user.password, password):
            login_user(user, remember=remember_me)
            return redirect(request.args.get("next") or url_for('main.show_first_page'))
        else:
            flash(gettext(MESSAGE_PASSWORD_IS_INCORRECT))

    return render_template('auth/login.html', form=login_form,
                           PASSWORD=PASSWORD,
                           EMAIL=EMAIL,
                           AUTHORIZATION=AUTHORIZATION,
                           LOGIN=LOGIN,
                           YOU_ALREADY_REGISTER=YOU_ALREADY_REGISTER)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
