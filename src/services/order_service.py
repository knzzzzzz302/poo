from src.models.order import Order, OrderItem, OrderStatus

class OrderService:
    
    def __init__(self, cart_service, product_service):
        self.orders = {}
        self.user_orders = {}
        self.cart_service = cart_service
        self.product_service = product_service
    
    def create_order_from_cart(self, cart_id, shipping_address, payment_method):
        cart = self.cart_service.get_cart_by_id(cart_id)
        
        if not cart or not cart.items:
            raise ValueError("Le panier est vide ou introuvable")
        
        if not shipping_address:
            raise ValueError("L'adresse de livraison est obligatoire")
        
        if not payment_method:
            raise ValueError("La méthode de paiement est obligatoire")
        
        for item in cart.items:
            if item.product.stock_quantity < item.quantity:
                raise ValueError(f"Stock insuffisant pour le produit '{item.product.name}'")
        
        order_items = []
        for item in cart.items:
            order_item = OrderItem(item.product, item.quantity, item.product.price)
            order_items.append(order_item)
            
            item.product.decrease_stock(item.quantity)
        
        order = Order(cart.user, order_items, shipping_address, payment_method)
        
        self.orders[order.id] = order
        
        if cart.user.id not in self.user_orders:
            self.user_orders[cart.user.id] = []
        self.user_orders[cart.user.id].append(order)
        
        cart.clear()
        
        return order
    
    def get_order_by_id(self, order_id):
        return self.orders.get(order_id)
    
    def get_orders_by_user_id(self, user_id):
        return self.user_orders.get(user_id, [])
    
    def update_order_status(self, order_id, status):
        order = self.get_order_by_id(order_id)
        
        if not order:
            return None
        
        if status == OrderStatus.CANCELLED and not order.can_cancel():
            raise ValueError("Cette commande ne peut plus être annulée")
        
        if status == OrderStatus.REFUNDED and not order.can_refund():
            raise ValueError("Cette commande ne peut pas être remboursée")
        
        if status == OrderStatus.CANCELLED:
            for item in order.items:
                product = self.product_service.get_product_by_id(item.product_id)
                if product:
                    product.increase_stock(item.quantity)
        
        order.update_status(status)
        
        return order
    
    def add_order_note(self, order_id, note):
        order = self.get_order_by_id(order_id)
        
        if not order or not note:
            return None
        
        order.add_note(note)
        return order
    
    def get_all_orders(self):
        return list(self.orders.values())
    
    def get_orders_by_status(self, status):
        return [order for order in self.orders.values() if order.status == status]
    
    def delete_order(self, order_id):
        order = self.get_order_by_id(order_id)
        
        if not order:
            return False
        
        if order.user_id in self.user_orders:
            self.user_orders[order.user_id] = [o for o in self.user_orders[order.user_id] if o.id != order_id]
        
        del self.orders[order_id]
        
        return True