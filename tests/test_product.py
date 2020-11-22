import datetime
import unittest
import os

from flask_pymongo import PyMongo
from mongomock import ObjectId as mockup_oid

from app import create_app

from mockupdb import MockupDB, go, Command
from pymongo import MongoClient
from json import dumps


class TestProductController(unittest.TestCase):
    @classmethod
    def setUpClass(self) -> None:
        self.server = MockupDB(auto_ismaster=True, verbose=True)
        self.server.run()

        class TestConfig:
            MONGO_URI = self.server.uri

        app = create_app(TestConfig)
        self.app = app.test_client()

    @classmethod
    def tearDownClass(self) -> None:
        self.server.stop()

    def test_create_product(self):
        to_insert = {
            "title": "First Aid kit",
            "description": "Your helper in journey",
            "params": {
                'price': 350,
                'class': 'B'
            }

        }
        headers = [('Content-Type', 'application/json')]
        with self.app as test_app:
            response = test_app.post('/api/product', json=to_insert, headers=headers)

        self.assertEqual(response.status_code, 201)
