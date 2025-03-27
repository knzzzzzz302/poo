import uuid
from datetime import datetime
from enum import Enum

class OrderStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class OrderItem:
    
    def __init__(self, product, quantity, price_at_purchase):
        self.id = str(uuid.uuid4())
        self.product_id = product.id
        self.product_name = product.name
        self.product_description = product.description
        self.quantity = quantity
        self.price_at_purchase = price_at_purchase
        self.created_at = datetime.now()
    
    def get_subtotal(self):
        return self.price_at_purchase * self.quantity
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'product_name': self.product_name,
            'product_description': self.product_description,
            'quantity': self.quantity,
            'price_at_purchase': self.price_at_purchase,
            'subtotal': self.get_subtotal(),
            'created_at': self.created_at.isoformat()
        }


class Order:
    
    def __init__(self, user, items, shipping_address, payment_method):
        self.id = str(uuid.uuid4())
        self.order_number = f"ORD-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
        self.user_id = user.id
        self.user_email = user.email
        self.items = items
        self.status = OrderStatus.PENDING
        self.shipping_address = shipping_address
        self.payment_method = payment_method
        self.subtotal = sum(item.get_subtotal() for item in items)
        self.discount = user.apply_discount(self.subtotal) - self.subtotal
        self.total = self.subtotal + self.discount
        self.created_at = datetime.now()
        self.updated_at = self.created_at
        self.shipped_at = None
        self.delivered_at = None
        self.cancelled_at = None
        self.refunded_at = None
        self.notes = []
    
    def update_status(self, status):
        self.status = status
        self.updated_at = datetime.now()
        
        if status == OrderStatus.SHIPPED:
            self.shipped_at = datetime.now()
        elif status == OrderStatus.DELIVERED:
            self.delivered_at = datetime.now()
        elif status == OrderStatus.CANCELLED:
            self.cancelled_at = datetime.now()
        elif status == OrderStatus.REFUNDED:
            self.refunded_at = datetime.now()
    
    def add_note(self, note):
        self.notes.append({
            'text': note,
            'timestamp': datetime.now()
        })
        self.updated_at = datetime.now()
    
    def can_cancel(self):
        return self.status in [OrderStatus.PENDING, OrderStatus.PROCESSING]
    
    def can_refund(self):
        return self.status in [OrderStatus.DELIVERED, OrderStatus.SHIPPED]
    
    def to_dict(self):
        return {
            'id': self.id,
            'order_number': self.order_number,
            'user_id': self.user_id,
            'user_email': self.user_email,
            'items': [item.to_dict() for item in self.items],
            'status': self.status.value,
            'shipping_address': self.shipping_address,
            'payment_method': self.payment_method,
            'subtotal': self.subtotal,
            'discount': self.discount,
            'total': self.total,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'shipped_at': self.shipped_at.isoformat() if self.shipped_at else None,
            'delivered_at': self.delivered_at.isoformat() if self.delivered_at else None,
            'cancelled_at': self.cancelled_at.isoformat() if self.cancelled_at else None,
            'refunded_at': self.refunded_at.isoformat() if self.refunded_at else None,
            'notes': self.notes
        }