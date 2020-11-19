from flask import jsonify, request, url_for
from flask_pymongo import ObjectId

from app.models import Product
from app.api import bp
from app import mongo
from app.api.errors import bad_request
from utils.db_utils import get_query_from_data


@bp.route('/product', methods=['POST'])
def create_product():
    """
    Method for create new product
    parameters:

    :return:
    """
    db_operations = mongo.db.product
    data = request.get_json(force=True) or {}
    if 'title' not in data or 'description' not in data or 'params' not in data:
        return bad_request('Must include title, description and params fields')

    new_product = Product()
    new_product.save_to_db(data, db_operations)

    response = jsonify(new_product.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_product_by_id', product_id=new_product.id)
    return response


@bp.route('/product', methods=['GET'])
def get_product_list():
    """
    Method for get list of product by title and/or params with pagination
    :return:
    """
    page = request.args.get('page', 0, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    db_operations = mongo.db.product
    data = request.get_json() or {}
    query_data = get_query_from_data(data)
    query = db_operations.find
    result = Product().to_collection_dict(query, query_data, page, per_page)
    return jsonify(result)


@bp.route('/product/<product_id>', methods=['GET'])
def get_product_by_id(product_id):
    """
    Method for get product by product_id
    :param product_id:
    :return:
    """
    if ObjectId().is_valid(product_id) is False:
        return bad_request('Invalid ID')
    db_operations = mongo.db.product
    product = db_operations.find_one_or_404({'_id': ObjectId(product_id)})
    response_product = Product().from_dict(product).to_dict()
    return jsonify(response_product)