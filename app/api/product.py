from app.api import bp
from app.models import Product


@bp.route('/product', methods=['POST'])
def create_product():
    """
    Method for create new product by title: str, description: str and params: dict

    :return:
    """
    response = Product.create_product()
    return response


@bp.route('/product', methods=['GET'])
def get_products():
    """
    Method for get list of product by title and/or params with pagination
    :return:
    """
    response = Product.get_products()
    return response


@bp.route('/product/<product_id>', methods=['GET'])
def get_product_by_id(product_id):
    """
    Method for get product by product_id
    :param product_id:
    :return:
    """
    response = Product.get_product_by_id(product_id)
    return response
