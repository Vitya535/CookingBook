"""Основные маршруты для JWT авторизации/аутентификации"""
from flask import redirect
from flask import render_template
from flask import url_for

from app.forms import LoginForm
from app.forms import RegistrationForm
from app.jwt import bp


@bp.route('/registration', methods=['GET', 'POST'])
def registration():
    registration_form = RegistrationForm()
    return render_template('jwt/registration.html', form=registration_form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    return render_template('jwt/login.html', form=login_form)


@bp.route('/logout', methods=['POST'])
def logout():
    return redirect(url_for('login'))
