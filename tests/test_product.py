import unittest
from json import dumps

from mockupdb import MockupDB, go

from app import create_app
from config import Config


class TestProductController(unittest.TestCase):
    @classmethod
    def setUpClass(self) -> None:
        self.server = MockupDB(auto_ismaster=True, verbose=True)
        self.server.run()

        Config.MONGO_URI = self.server.uri

        app = create_app()
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

        go(self.app.post, '/api/product', data=dumps(to_insert), headers=headers)
        rv = self.server.receives()
        new_object_id = str(rv.docs[0]['documents'][0]['_id'])
        go(self.app.get, f'/api/product/{new_object_id}', headers=headers)
        request = self.server.receives()
        request_status = request.ok(cursor={'id': new_object_id, 'firstBatch': [
            to_insert
        ]})
        self.assertTrue(request_status)

