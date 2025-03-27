from flask import Blueprint, request, jsonify, session
from src.services.cart_service import CartService
from src.services.user_service import UserService

cart_bp = Blueprint('cart', __name__)
cart_service = CartService(None)  
user_service = UserService()

@cart_bp.route('/api/cart/add', methods=['POST'])
def api_add_to_cart():
    user_id = request.headers.get('X-User-ID')
    data = request.get_json()
    
    user = user_service.get_user_by_id(user_id)
    if not user:
        return jsonify({'success': False, 'message': 'Utilisateur introuvable'}), 404
    
    cart = cart_service.get_cart_by_user_id(user.id) or cart_service.create_cart(user)
    if cart_service.add_item_to_cart(cart.id, data.get('product_id'), data.get('quantity', 1)):
        return jsonify({'success': True, 'cart': cart.to_dict()})
    
    return jsonify({'success': False, 'message': 'Erreur d\'ajout au panier'}), 400

@cart_bp.route('/api/cart', methods=['GET'])
def api_get_cart():
    user_id = request.headers.get('X-User-ID')
    user = user_service.get_user_by_id(user_id)
    if not user:
        return jsonify({'success': False, 'message': 'Utilisateur introuvable'}), 404
    
    cart = cart_service.get_cart_by_user_id(user.id)
    return jsonify({'success': True, 'cart': cart.to_dict() if cart else {}})