#app/__init__.py: Ініціалізує Flask-додаток та налаштування бази даних.

from flask import Flask
from config import Config

app = Flask(__name__, static_url_path='/static', static_folder='static', )
app.config.from_object(Config)

from app import routes
