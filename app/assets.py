"""Генерация CSS, JS файлов в один"""
from flask_assets import Bundle
from flask_assets import Environment

BUNDLES = {
    'jquery-confirm_fontawesome_custom_css': Bundle(
        'https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.5.0/css/bootstrap.min.css',
        'https://cdnjs.cloudflare.com/ajax/libs/jquery-confirm/3.3.4/jquery-confirm.min.css',
        'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.13.1/css/solid.min.css',
        'css/common.css',
        output='gen/jquery-confirm_fontawesome_custom.css',
        filters='cssmin'
    ),
    'popper_bootstrap_jquery-confirm_js': Bundle(
        'https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.min.js',
        'https://cdnjs.cloudflare.com/ajax/libs/popper.js/2.4.2/umd/popper.min.js',
        'https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.5.0/js/bootstrap.min.js',
        'https://cdnjs.cloudflare.com/ajax/libs/jquery-confirm/3.3.4/jquery-confirm.min.js',
        'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.13.1/js/fontawesome.min.js',
        'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.13.1/js/solid.min.js',
        'js/sw_register.js',
        output='gen/popper_bootstrap_jquery-confirm.js',
        filters='jsmin'
    )
}

ASSETS = Environment()
ASSETS.register(BUNDLES)
