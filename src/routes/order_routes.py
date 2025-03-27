from flask import Blueprint, request, jsonify
from src.services.order_service import OrderService
from src.services.user_service import UserService
from src.models.order import OrderStatus

order_bp = Blueprint('order', __name__)
order_service = OrderService(None, None)  
user_service = UserService()

@order_bp.route('/api/checkout', methods=['POST'])
def api_checkout():
    user_id = request.headers.get('X-User-ID')
    data = request.get_json()
    
    user = user_service.get_user_by_id(user_id)
    if not user:
        return jsonify({'success': False, 'message': 'Utilisateur introuvable'}), 404
    
    try:
        cart = cart_service.get_cart_by_user_id(user.id)
        if not cart or not cart.items:
            return jsonify({'success': False, 'message': 'Panier vide'}), 400
        
        order = order_service.create_order_from_cart(
            cart.id, data.get('shipping_address'), data.get('payment_method')
        )
        return jsonify({'success': True, 'order': order.to_dict()}), 201
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@order_bp.route('/api/orders/<order_id>', methods=['GET'])
def api_order_detail(order_id):
    user_id = request.headers.get('X-User-ID')
    user = user_service.get_user_by_id(user_id)
    if not user:
        return jsonify({'success': False, 'message': 'Utilisateur introuvable'}), 404
    
    order = order_service.get_order_by_id(order_id)
    if not order:
        return jsonify({'success': False, 'message': 'Commande introuvable'}), 404
    
    if order.user_id != user.id:
        return jsonify({'success': False, 'message': 'Accès non autorisé'}), 403
    
    return jsonify({'success': True, 'order': order.to_dict()})