import uuid
from datetime import datetime

class CartItem:
    
    def __init__(self, product, quantity=1):
        self.id = str(uuid.uuid4())
        self.product = product
        self.quantity = quantity
        self.added_at = datetime.now()
        self.updated_at = self.added_at
    
    def update_quantity(self, quantity):
        self.quantity = quantity
        self.updated_at = datetime.now()
    
    def get_subtotal(self):
        return self.product.price * self.quantity
    
    def to_dict(self):
        return {
            'id': self.id,
            'product': self.product.to_dict(),
            'quantity': self.quantity,
            'subtotal': self.get_subtotal(),
            'added_at': self.added_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class Cart:
    
    def __init__(self, user):
        self.id = str(uuid.uuid4())
        self.user = user
        self.items = []
        self.created_at = datetime.now()
        self.updated_at = self.created_at
    
    def add_item(self, product, quantity=1):
        if not product.is_in_stock() or product.stock_quantity < quantity:
            return False
        
        for item in self.items:
            if item.product.id == product.id:
                item.update_quantity(item.quantity + quantity)
                self.updated_at = datetime.now()
                return True
        
        self.items.append(CartItem(product, quantity))
        self.updated_at = datetime.now()
        return True
    
    def remove_item(self, item_id):
        initial_length = len(self.items)
        self.items = [item for item in self.items if item.id != item_id]
        
        if len(self.items) < initial_length:
            self.updated_at = datetime.now()
            return True
        return False
    
    def update_item_quantity(self, item_id, quantity):
        for item in self.items:
            if item.id == item_id:
                if item.product.stock_quantity >= quantity:
                    item.update_quantity(quantity)
                    self.updated_at = datetime.now()
                    return True
                return False
        return False
    
    def clear(self):
        self.items = []
        self.updated_at = datetime.now()
    
    def get_total(self):
        return sum(item.get_subtotal() for item in self.items)
    
    def get_total_with_discount(self):
        total = self.get_total()
        return self.user.apply_discount(total)
    
    def get_item_count(self):
        return sum(item.quantity for item in self.items)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user.id,
            'items': [item.to_dict() for item in self.items],
            'total': self.get_total(),
            'total_with_discount': self.get_total_with_discount(),
            'item_count': self.get_item_count(),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }