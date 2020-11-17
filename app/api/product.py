from flask import jsonify, request, url_for

from app.models import Product

from app.api import bp
from app import mongo
from app.api.errors import bad_request


@bp.route('/product', methods=['POST'])
def create_product():
    db_operations = mongo.db.product
    data = request.get_json() or {}
    if 'title' not in data or 'title' not in data:
        return bad_request('Must include title, price and type fields')

    new_product = Product()
    new_product.save_to_db(data, db_operations)

    response = jsonify(new_product.to_dict())
    response.status_code = 201
    # response.headers['Location'] = url_for('front_api.get_product', product_id=product.id)
    return response


@bp.route('/product/list', methods=['GET'])
def get_product_list():
    db_operations = mongo.db.product
    data = request.get_json() or {}
    if 'params' in data and 'title' in data:
        key = next(iter(data['params']))
        value = str(data['params'][key])
        results = db_operations.find({f'params.{key}': value, 'title': data['title']})
        result_list = [Product().from_dict(r).to_dict() for r in results]
        return jsonify(result_list)
    elif 'title' in data:
        results = db_operations.find({'title': data['title']})
        result_list = [Product().from_dict(r).to_dict() for r in results]
        return jsonify(result_list)
    elif 'params' in data:
        key = next(iter(data['params']))
        value = str(data['params'][key])
        results = db_operations.find({f'params.{key}': value})
        result_list = [Product().from_dict(r).to_dict() for r in results]
        return jsonify(result_list)
    else:
        results = db_operations.find()
        result_list = [Product().from_dict(r).to_dict() for r in results]
        return jsonify(result_list)