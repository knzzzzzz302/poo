from abc import ABC, abstractmethod
import uuid
from datetime import datetime
import hashlib

class User(ABC):
    
    def __init__(self, username, email, password):
        self.id = str(uuid.uuid4())
        self.username = username
        self.email = email
        self.password_hash = self._hash_password(password)
        self.created_at = datetime.now()
        self.cart_items = []
    
    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password):
        return self._hash_password(password) == self.password_hash
    
    def add_to_cart(self, product, quantity=1):
        for item in self.cart_items:
            if item['product'].id == product.id:
                item['quantity'] += quantity
                return
        
        self.cart_items.append({
            'product': product,
            'quantity': quantity
        })
    
    def remove_from_cart(self, product_id):
        self.cart_items = [item for item in self.cart_items 
                          if item['product'].id != product_id]
    
    def get_cart_total(self):
        total = sum(item['product'].price * item['quantity'] 
                   for item in self.cart_items)
        return self.apply_discount(total)
    
    @abstractmethod
    def apply_discount(self, amount):
        pass


class RegularUser(User):
    
    def apply_discount(self, amount):
        return amount


class PremiumUser(User):
    
    def __init__(self, username, email, password):
        super().__init__(username, email, password)
        self.discount_rate = 0.10
    
    def apply_discount(self, amount):
        return amount * (1 - self.discount_rate)


class BusinessUser(User):
    
    def __init__(self, username, email, password, company_name):
        super().__init__(username, email, password)
        self.company_name = company_name
        self.discount_rate = 0.20
    
    def apply_discount(self, amount):
        return amount * (1 - self.discount_rate)