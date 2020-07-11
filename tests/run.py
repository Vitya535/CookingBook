"""Файл для выполнения всех тестов в приложении"""
from os.path import dirname
from unittest import TestLoader
from unittest import TextTestRunner

if __name__ == '__main__':
    suite = TestLoader().discover(dirname(__file__))
    runner = TextTestRunner()
    runner.run(suite)
