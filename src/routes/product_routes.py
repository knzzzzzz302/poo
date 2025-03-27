from flask import Blueprint, request, jsonify, render_template
from src.services.product_service import ProductService

product_bp = Blueprint('product', __name__)
product_service = ProductService()

@product_bp.route('/')
def list_products():
    products = product_service.get_all_products()
    return render_template('products/list.html', products=products)

@product_bp.route('/<product_id>')
def product_detail(product_id):
    product = product_service.get_product_by_id(product_id)
    return render_template('products/detail.html', product=product)

@product_bp.route('/api/products', methods=['GET'])
def api_list_products():
    products = product_service.get_all_products()
    return jsonify({'success': True, 'products': [p.to_dict() for p in products]})

@product_bp.route('/api/products/<product_id>', methods=['GET'])
def api_product_detail(product_id):
    product = product_service.get_product_by_id(product_id)
    if product:
        return jsonify({'success': True, 'product': product.to_dict()})
    return jsonify({'success': False, 'message': 'Produit non trouvé'}), 404