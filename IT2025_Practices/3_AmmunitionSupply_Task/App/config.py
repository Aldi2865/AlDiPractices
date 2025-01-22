

import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '333'
    DATABASE_USER = 'postgres'  # Змінено на 'postgres'
    DATABASE_PASSWORD = 'admin'  # Змінено на 'admin'