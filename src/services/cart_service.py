from src.models.cart import Cart

class CartService:
    
    def __init__(self, product_service):
        self.carts = {}
        self.user_carts = {}
        self.product_service = product_service
    
    def create_cart(self, user):
        if user.id in self.user_carts:
            return self.user_carts[user.id]
        
        cart = Cart(user)
        
        self.carts[cart.id] = cart
        self.user_carts[user.id] = cart
        
        return cart
    
    def get_cart_by_id(self, cart_id):
        return self.carts.get(cart_id)
    
    def get_cart_by_user_id(self, user_id):
        return self.user_carts.get(user_id)
    
    def add_item_to_cart(self, cart_id, product_id, quantity=1):
        cart = self.get_cart_by_id(cart_id)
        product = self.product_service.get_product_by_id(product_id)
        
        if not cart or not product:
            return False
        
        return cart.add_item(product, quantity)
    
    def remove_item_from_cart(self, cart_id, item_id):
        cart = self.get_cart_by_id(cart_id)
        
        if not cart:
            return False
        
        return cart.remove_item(item_id)
    
    def update_item_quantity(self, cart_id, item_id, quantity):
        cart = self.get_cart_by_id(cart_id)
        
        if not cart or quantity < 1:
            return False
        
        return cart.update_item_quantity(item_id, quantity)
    
    def clear_cart(self, cart_id):
        cart = self.get_cart_by_id(cart_id)
        
        if not cart:
            return False
        
        cart.clear()
        return True
    
    def get_cart_total(self, cart_id):
        cart = self.get_cart_by_id(cart_id)
        
        if not cart:
            return None
        
        return cart.get_total()
    
    def get_cart_total_with_discount(self, cart_id):
        cart = self.get_cart_by_id(cart_id)
        
        if not cart:
            return None
        
        return cart.get_total_with_discount()
    
    def merge_carts(self, source_cart_id, target_cart_id):
        source_cart = self.get_cart_by_id(source_cart_id)
        target_cart = self.get_cart_by_id(target_cart_id)
        
        if not source_cart or not target_cart:
            return False
        
        for item in source_cart.items:
            target_cart.add_item(item.product, item.quantity)
        
        source_cart.clear()
        
        return True
    
    def delete_cart(self, cart_id):
        cart = self.get_cart_by_id(cart_id)
        
        if not cart:
            return False
        
        del self.carts[cart_id]
        del self.user_carts[cart.user.id]
        
        return True