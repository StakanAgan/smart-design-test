import os

from dotenv import load_dotenv

load_dotenv('.env')


class Config:
    MONGO_URI = os.environ.get('MONGO_URI')
    TESTING = os.environ.get('TESTING', False)
