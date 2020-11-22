import os

from dotenv import load_dotenv

load_dotenv('.env')


class Config:
    MONGO_URI = os.environ.get('MONGO_URI')
    SECRET_KEY = os.environ.get('SECRET_KEY')


class TestConfig:
    MONGO_URI = os.environ.get('MONGO_URI')
    TESTING = True
