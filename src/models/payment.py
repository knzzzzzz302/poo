from abc import ABC, abstractmethod
from typing import Dict, Any
from .order import Order

class PaymentMethod(ABC):
    @abstractmethod
    def process_payment(self, order: Order) -> bool:
        pass
    
    @abstractmethod
    def get_payment_details(self) -> Dict[str, Any]:
        pass


class CreditCard(PaymentMethod):
    def __init__(self, card_number: str, expiry_date: str, cvv: str):
        self.__card_number = card_number
        self.__expiry_date = expiry_date
        self.__cvv = cvv
    
    def process_payment(self, order: Order) -> bool:
        print(f"Traitement du paiement par carte de crédit pour la commande {order.order_id}")
        return True
    
    def get_payment_details(self) -> Dict[str, Any]:
        return {
            "method": "credit_card",
            "card_number": f"****-****-****-{self.__card_number[-4:]}",
            "expiry_date": self.__expiry_date
        }


class PayPal(PaymentMethod):
    def __init__(self, email: str):
        self.__email = email
    
    def process_payment(self, order: Order) -> bool:
        print(f"Traitement du paiement par PayPal pour la commande {order.order_id}")
        return True
    
    def get_payment_details(self) -> Dict[str, Any]:
        return {
            "method": "paypal",
            "email": self.__email
        }