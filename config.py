#config.py
from dotenv import load_dotenv
import os

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'erraetst-du-nie'
    SERVER_NAME = 'kochrezept-docker.engeli.me'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
