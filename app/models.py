from collections import OrderedDict

import flask
from flask_pymongo import ObjectId, MongoClient
from flask import request, jsonify, url_for

from static.text.api import text as t
from app.errors import bad_request
from config import Config


PER_PAGE_DEFAULT = 10
PER_PAGE_MAX = 100
DEFAULT_PAGE = 0


class PaginatedAPIMixin:
    @classmethod
    def to_collection_dict(cls, query, data, page, per_page):
        """
        Method for make query to MongoDB with pagination and return
        data in response
        :param query:
        :param data:
        :param page:
        :param per_page:
        :return:
        """
        resources = query(data).skip(page * per_page).limit(per_page)
        data = {
            'items': [cls().to_response(item) for item in resources],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_items': resources.count()
            }
        }
        return data

    def to_response(self, data):
        pass


class Product(PaginatedAPIMixin):
    def __init__(self, title=None, description=None, params=None):
        self._id = None
        self.title = title
        self.description = description
        self.params = params

    def __repr__(self):
        return f'Product {self.title}'

    @staticmethod
    def create_product():
        """
        Method for product creation by request
        :return:
        """
        mongo = MongoClient(Config.MONGO_URI)
        db_operations = mongo.db.product
        data = request.get_json(force=True) or {}
        if 'title' not in data or 'description' not in data or 'params' not in data:
            return bad_request(t['empty_field'])
        new_product = Product()
        if Product.params_is_valid(data):
            new_product.save_to_db(data, db_operations)

            response = jsonify(new_product.to_dict())
            response.status_code = 201
            response.headers['Location'] = url_for('api.get_product_by_id', product_id=new_product._id)
            return response
        else:
            return bad_request(t['invalid_value'])

    @staticmethod
    def get_products():
        """
        Method for get product list with pagination by params: dict and/or title: str
        :return:
        """
        mongo = MongoClient(Config.MONGO_URI)
        page = request.args.get('page', DEFAULT_PAGE, type=int)
        per_page = min(request.args.get('per_page', PER_PAGE_DEFAULT, type=int), PER_PAGE_MAX)
        db_operations = mongo.db.product
        data = {k: v for k, v in request.args.items() if k not in ['page', 'per_page']}
        query_data = Product.get_query_from_data(data)
        query = db_operations.find
        result = Product().to_collection_dict(query, query_data, page, per_page)
        return jsonify(result)

    @staticmethod
    def _set_query_params(query, key, value):
        """
        Method for set params in query to mongoDB like
        {param.key: "value"}
        :param query:
        :param key:
        :param value:
        :return:
        """
        query.update({str(key): str(value)})

    @staticmethod
    def get_query_from_data(data):
        """
        Form query to mongoDB from request data for searching objects
        :param data:
        :return:
        """
        query_params = {}
        for key, value in data.items():
            if key == 'title':
                Product._set_query_params(query_params, key, value)
            elif isinstance(value, str):
                param_key = f'params.{str(key)}'
                Product._set_query_params(query_params, param_key, value)
        return query_params

    @staticmethod
    def get_product_by_id(product_id):
        """
        Method for finding product by id
        :param product_id:
        :return:
        """
        mongo = MongoClient(Config.MONGO_URI)
        if ObjectId().is_valid(product_id) is False:
            return bad_request(t['invalid_id'])
        db_operations = mongo.db.product
        product = db_operations.find_one_or_404({'_id': ObjectId(product_id)})
        response_product = Product().from_dict(product).to_dict()
        return jsonify(response_product)

    def to_dict(self):
        """
        Method for represent Product object into dict for use in API
        :return:
        """
        data = OrderedDict({
            'title': str(self.title),
            'description': str(self.description),
            'params': {str(key): str(value) for key, value in self.params.items()}
        })
        if self._id:
            data.update({"id": str(self._id)})
        return data

    def from_dict(self, data):
        """
        Method for set Product attributes from dict object
        :param data:
        :return:
        """
        for field in ['_id', 'title', 'description', 'params']:
            if field in data:
                setattr(self, field, data[field])
        return self

    def to_response(self, data):
        """
        Method for represent Product object in response.content form
        :param data:
        :return:
        """
        return self.from_dict(data).to_dict()

    def save_to_db(self, data, db_operations):
        """
        Method for save Product object into mongoDB and get id this Product
        :param data:
        :param db_operations:
        :return:
        """
        self.from_dict(data)
        self._id = str(db_operations.insert_one(self.to_dict()).inserted_id)

    @staticmethod
    def params_is_valid(data):
        """
        Method for validation request data
        :param data:
        :return:
        """
        if isinstance(data['title'], str) and isinstance(data['description'], str) and isinstance(data['params'], dict):
            return True
        else:
            return False
