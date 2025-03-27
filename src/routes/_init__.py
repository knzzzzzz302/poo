
from src.routes.user_routes import user_bp
from src.routes.product_routes import product_bp
from src.routes.cart_routes import cart_bp
from src.routes.order_routes import order_bp

__all__ = [
    'user_bp',
    'product_bp',
    'cart_bp',
    'order_bp'
]