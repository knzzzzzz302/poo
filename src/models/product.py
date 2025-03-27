import uuid
from datetime import datetime

class Product:
    
    def __init__(self, name, description, price, stock_quantity):
        self.id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.price = price
        self.stock_quantity = stock_quantity
        self.created_at = datetime.now()
        self.updated_at = self.created_at
        self.is_active = True
        self.categories = []
    
    def update(self, name=None, description=None, price=None, stock_quantity=None):
        if name is not None:
            self.name = name
        
        if description is not None:
            self.description = description
        
        if price is not None:
            self.price = price
        
        if stock_quantity is not None:
            self.stock_quantity = stock_quantity
        
        self.updated_at = datetime.now()
    
    def add_to_category(self, category):
        if category not in self.categories:
            self.categories.append(category)
    
    def remove_from_category(self, category):
        if category in self.categories:
            self.categories.remove(category)
    
    def is_in_stock(self):
        return self.stock_quantity > 0
    
    def decrease_stock(self, quantity=1):
        if self.stock_quantity >= quantity:
            self.stock_quantity -= quantity
            self.updated_at = datetime.now()
            return True
        return False
    
    def increase_stock(self, quantity=1):
        self.stock_quantity += quantity
        self.updated_at = datetime.now()
    
    def activate(self):
        self.is_active = True
        self.updated_at = datetime.now()
    
    def deactivate(self):
        self.is_active = False
        self.updated_at = datetime.now()
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'stock_quantity': self.stock_quantity,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'is_active': self.is_active,
            'categories': [category.name for category in self.categories]
        }


class Category:
    
    def __init__(self, name, description=""):
        self.id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.created_at = datetime.now()
        self.updated_at = self.created_at
        self.products = []
    
    def add_product(self, product):
        if product not in self.products:
            self.products.append(product)
            product.add_to_category(self)
    
    def remove_product(self, product):
        if product in self.products:
            self.products.remove(product)
            product.remove_from_category(self)
    
    def update(self, name=None, description=None):
        if name is not None:
            self.name = name
        
        if description is not None:
            self.description = description
        
        self.updated_at = datetime.now()
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'products_count': len(self.products)
        }