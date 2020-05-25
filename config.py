from os import getenv, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv()


class Config:
    FLASK_APP = 'wsgi.py'
    FLASK_ENV = getenv('FLASK_ENV')
    SECRET_KEY = getenv('SECRET_KEY')
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    COMPRESSOR_DEBUG = True