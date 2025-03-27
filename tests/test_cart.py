import unittest
from src.models.user import User
from src.models.product import Product
from src.models.cart import Cart
from src.services.cart_service import CartService

class TestCart(unittest.TestCase):
    def setUp(self):
        self.user = User("jean_dupont", "jean@example.com", "MotDePasse123!")
        self.cart = Cart(self.user)
        self.product1 = Product("Ordinateur", 999.99, 10)
        self.product2 = Product("Smartphone", 599.99, 20)

    def test_add_product(self):
        self.cart.add_product(self.product1, 2)
        self.assertIn(self.product1, self.cart.items)
        self.assertEqual(self.cart.items[self.product1], 2)

    def test_remove_product(self):
        self.cart.add_product(self.product1, 3)
        self.cart.remove_product(self.product1, 1)
        self.assertEqual(self.cart.items[self.product1], 2)

    def test_calculate_total(self):
        self.cart.add_product(self.product1, 2)
        self.cart.add_product(self.product2, 1)
        expected_total = (2 * 999.99) + (1 * 599.99)
        self.assertAlmostEqual(self.cart.calculate_total(), expected_total)

if __name__ == '__main__':
    unittest.main()