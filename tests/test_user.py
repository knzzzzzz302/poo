import unittest
from src.models.user import User
from src.services.user_service import UserService

class TestUser(unittest.TestCase):
    def setUp(self):
        self.user_service = UserService()

    def test_user_creation(self):
        user = self.user_service.register_user(
            "jean_dupont", 
            "jean@example.com", 
            "MotDePasse123!"
        )
        self.assertIsNotNone(user)
        self.assertEqual(user.username, "jean_dupont")
        self.assertEqual(user.email, "jean@example.com")

    def test_login(self):
        user = self.user_service.register_user(
            "jean_dupont", 
            "jean@example.com", 
            "MotDePasse123!"
        )
        logged_user = self.user_service.login("jean@example.com", "MotDePasse123!")
        self.assertEqual(user, logged_user)

    def test_invalid_login(self):
        self.user_service.register_user(
            "jean_dupont", 
            "jean@example.com", 
            "MotDePasse123!"
        )
        with self.assertRaises(ValueError):
            self.user_service.login("jean@example.com", "WrongPassword")

if __name__ == '__main__':
    unittest.main()