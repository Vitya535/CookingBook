"""Генерация CSS, JS файлов в один"""
from flask_assets import Environment, Bundle

CSS = Bundle('css_files/style_table_view.css', output='gen_files/gen_style_file.css', filters='cssmin')
JS = Bundle('js_files/jquery-3.3.1.min.js', 'js_files/jquery.tablesorter.js',
            output='gen_files/gen_script_file.js', filters='jsmin')
ASSETS = Environment()
ASSETS.register('gen_style_file', CSS)
ASSETS.register('gen_script_file', JS)
