from src.models.product import Product, Category

class ProductService:
    
    def __init__(self):
        self.products = {}
        self.categories = {}
    
    def add_product(self, name, description, price, stock_quantity):
        if not name:
            raise ValueError("Le nom du produit est obligatoire")
        
        if price < 0:
            raise ValueError("Le prix ne peut pas être négatif")
        
        if stock_quantity < 0:
            raise ValueError("La quantité en stock ne peut pas être négative")
        
        product = Product(name, description, price, stock_quantity)
        
        self.products[product.id] = product
        
        return product
    
    def get_product_by_id(self, product_id):
        return self.products.get(product_id)
    
    def update_product(self, product_id, name=None, description=None, price=None, stock_quantity=None):
        product = self.get_product_by_id(product_id)
        
        if not product:
            return None
        
        if price is not None and price < 0:
            raise ValueError("Le prix ne peut pas être négatif")
        
        if stock_quantity is not None and stock_quantity < 0:
            raise ValueError("La quantité en stock ne peut pas être négative")
        
        product.update(name, description, price, stock_quantity)
        
        return product
    
    def delete_product(self, product_id):
        if product_id not in self.products:
            return False
        
        product = self.products[product_id]
        for category in list(product.categories):
            category.remove_product(product)
        
        del self.products[product_id]
        
        return True
    
    def get_all_products(self):
        return list(self.products.values())
    
    def search_products(self, query):
        query = query.lower()
        results = []
        
        for product in self.products.values():
            if query in product.name.lower() or query in product.description.lower():
                results.append(product)
        
        return results
    
    def add_category(self, name, description=""):
        if not name:
            raise ValueError("Le nom de la catégorie est obligatoire")
        
        for category in self.categories.values():
            if category.name.lower() == name.lower():
                raise ValueError("Une catégorie avec ce nom existe déjà")
        
        category = Category(name, description)
        
        self.categories[category.id] = category
        
        return category
    
    def get_category_by_id(self, category_id):
        return self.categories.get(category_id)
    
    def update_category(self, category_id, name=None, description=None):
        category = self.get_category_by_id(category_id)
        
        if not category:
            return None
        
        if name:
            for cat in self.categories.values():
                if cat.id != category_id and cat.name.lower() == name.lower():
                    raise ValueError("Une catégorie avec ce nom existe déjà")
        
        category.update(name, description)
        
        return category
    
    def delete_category(self, category_id):
        if category_id not in self.categories:
            return False
        
        category = self.categories[category_id]
        for product in list(category.products):
            product.remove_from_category(category)
        
        del self.categories[category_id]
        
        return True
    
    def get_all_categories(self):
        return list(self.categories.values())
    
    def add_product_to_category(self, product_id, category_id):
        product = self.get_product_by_id(product_id)
        category = self.get_category_by_id(category_id)
        
        if not product or not category:
            return False
        
        category.add_product(product)
        return True
    
    def remove_product_from_category(self, product_id, category_id):
        product = self.get_product_by_id(product_id)
        category = self.get_category_by_id(category_id)
        
        if not product or not category:
            return False
        
        category.remove_product(product)
        return True
    
    def get_products_by_category(self, category_id):
        category = self.get_category_by_id(category_id)
        
        if not category:
            return []
        
        return category.products.copy()