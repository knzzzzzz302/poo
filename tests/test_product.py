import unittest
from src.models.product import Product
from src.services.product_service import ProductService

class TestProduct(unittest.TestCase):
    def setUp(self):
        self.product_service = ProductService()

    def test_product_creation(self):
        product = self.product_service.add_product(
            "Ordinateur Portable", 
            999.99, 
            10
        )
        self.assertIsNotNone(product)
        self.assertEqual(product.name, "Ordinateur Portable")
        self.assertEqual(product.price, 999.99)
        self.assertEqual(product._stock_quantity, 10)

    def test_update_stock(self):
        product = self.product_service.add_product(
            "Smartphone", 
            599.99, 
            20
        )
        product.update_stock(-5)
        self.assertEqual(product._stock_quantity, 15)

    def test_get_product_details(self):
        product = self.product_service.add_product(
            "Tablette", 
            299.99, 
            15
        )
        details = product.get_product_details()
        self.assertIn("id", details)
        self.assertIn("name", details)
        self.assertIn("price", details)
        self.assertIn("stock", details)

if __name__ == '__main__':
    unittest.main()