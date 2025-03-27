import unittest
from src.models.user import User
from src.models.product import Product
from src.models.cart import Cart
from src.models.order import Order
from src.services.order_service import OrderService

class TestOrder(unittest.TestCase):
    def setUp(self):
        self.user = User("jean_dupont", "jean@example.com", "MotDePasse123!")
        self.product1 = Product("Ordinateur", 999.99, 10)
        self.product2 = Product("Smartphone", 599.99, 20)
        self.cart = Cart(self.user)
        self.order_service = OrderService()

    def test_place_order(self):
        self.cart.add_product(self.product1, 2)
        self.cart.add_product(self.product2, 1)

        order = self.order_service.place_order(self.cart)
        
        self.assertIsNotNone(order)
        self.assertEqual(order.status, "confirmed")
        self.assertEqual(len(order.items), 2)

    def test_order_status_update(self):
        self.cart.add_product(self.product1, 2)
        order = self.order_service.place_order(self.cart)
        
        order.update_status("shipped")
        self.assertEqual(order.status, "shipped")

if __name__ == '__main__':
    unittest.main()