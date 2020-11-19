from collections import OrderedDict

from bson import ObjectId
from flask import request, jsonify, url_for

from app import mongo
from app.errors import bad_request
from utils.db_utils import get_query_from_data


class PaginatedAPIMixin:
    @classmethod
    def to_collection_dict(cls, query, data, page, per_page, **kwargs):
        resources = query(data).skip(page * per_page).limit(per_page)
        data = {
            'items': [cls().to_response(item) for item in resources],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_items': query().count()
            }
        }
        return data

    def to_response(self, data):
        pass


class Product(PaginatedAPIMixin):
    def __init__(self, title=None, description=None, params=None):
        self.id = None
        self.title = title
        self.description = description
        self.params = params

    def __repr__(self):
        return f'Product {self.title}'

    @staticmethod
    def create_product():
        db_operations = mongo.db.product
        data = request.get_json(force=True) or {}
        if 'title' not in data or 'description' not in data or 'params' not in data:
            return bad_request('Must include title, description and params fields')

        new_product = Product()
        if Product.params_is_valid(data):
            new_product.save_to_db(data, db_operations)

            response = jsonify(new_product.to_dict())
            response.status_code = 201
            response.headers['Location'] = url_for('api.get_product_by_id', product_id=new_product.id)
            return response
        else:
            return bad_request('Value is not valid')

    @staticmethod
    def get_products():
        page = request.args.get('page', 0, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 100)
        db_operations = mongo.db.product
        data = {k: v for k, v in request.args.items() if k not in ['page', 'per_page']}
        query_data = Product.get_query_from_data(data)
        query = db_operations.find
        result = Product().to_collection_dict(query, query_data, page, per_page)
        return jsonify(result)

    @staticmethod
    def get_query_from_data(data):
        query_params = {}
        for key, value in data.items():
            if key == 'title' and isinstance(value, str) or isinstance(value, float):
                query_params.update({str(key): str(value)})
            elif isinstance(value, str) or isinstance(value, float):
                query_params.update({f'params.{str(key)}': str(value)})
            elif isinstance(value, dict):
                data_key = next(iter(data[key]))
                value = str(data[key][data_key])
                query_params.update({f'{str(key)}.{str(data_key)}': str(value)})
        return query_params

    @staticmethod
    def get_product_by_id(product_id):
        if ObjectId().is_valid(product_id) is False:
            return bad_request('Invalid ID')
        db_operations = mongo.db.product
        product = db_operations.find_one_or_404({'_id': ObjectId(product_id)})
        response_product = Product().from_dict(product).to_dict()
        return jsonify(response_product)

    def to_dict(self):
        data = OrderedDict({
            'title': self.title,
            'description': self.description,
            'params': {key: value for key, value in self.params.items()}
        })
        if self.id:
            data.update({"id": str(self.id)})
            data.move_to_end('id', last=False)
        return data

    def from_dict(self, data):
        for field in ['title', 'description', 'params']:
            if field in data:
                setattr(self, field, data[field])
        if '_id' in data:
            setattr(self, 'id', data['_id'])
        return self

    def to_response(self, data):
        return self.from_dict(data).to_dict()

    def save_to_db(self, data, db_operations):
        self.from_dict(data)
        self.id = str(db_operations.insert_one(self.to_dict()).inserted_id)

    @staticmethod
    def params_is_valid(data):
        if isinstance(data['title'], str) and isinstance(data['description'], str) and isinstance(data['params'], dict):
            return True
        else:
            return False
