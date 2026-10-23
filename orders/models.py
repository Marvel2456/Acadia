import uuid
from decimal import Decimal
from django.db import models
from django.utils import timezone
from catalog.models import Product, ProductVariation


class Order(models.Model):
    FULFILMENT_CHOICES = [
        ('pickup', 'Self-Pickup at Bakery'),
        ('delivery', 'Doorstep Delivery'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('bank_transfer', 'Direct Bank Transfer (Account Details Provided)'),
        ('paystack', 'Paystack (Cards, Bank Transfer, USSD)'),
        ('cash_on_pickup', 'Pay on Store Pickup'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Awaiting Payment'),
        ('paid', 'Paid & Confirmed'),
        ('failed', 'Payment Failed'),
        ('refunded', 'Refunded'),
    ]

    FULFILMENT_STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('confirmed', 'Order Confirmed'),
        ('preparing', 'Baking & Preparing'),
        ('ready_for_pickup', 'Ready for Pickup'),
        ('out_for_delivery', 'Out for Delivery'),
        ('completed', 'Delivered / Completed'),
        ('cancelled', 'Cancelled'),
    ]

    order_number = models.CharField(max_length=32, unique=True, editable=False)
    customer_name = models.CharField(max_length=150)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=30)
    fulfilment_type = models.CharField(max_length=20, choices=FULFILMENT_CHOICES, default='delivery')
    delivery_address = models.TextField(blank=True)
    delivery_city = models.CharField(max_length=100, blank=True, default='Lagos')
    preferred_date = models.DateField(null=True, blank=True)
    preferred_time_slot = models.CharField(max_length=100, blank=True, default='Morning (9:00 AM – 1:00 PM)')
    special_notes = models.TextField(blank=True, help_text="Any allergies, custom message on packaging, or special requests")
    
    # Financial fields calculated strictly on server
    subtotal_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    
    # Payment & Fulfilment
    payment_method = models.CharField(max_length=30, choices=PAYMENT_METHOD_CHOICES, default='bank_transfer')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    fulfilment_status = models.CharField(max_length=30, choices=FULFILMENT_STATUS_CHOICES, default='pending')
    paystack_reference = models.CharField(max_length=120, blank=True, db_index=True)
    
    internal_notes = models.TextField(blank=True, help_text="Notes for kitchen and dispatch team")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.order_number:
            date_str = timezone.now().strftime('%Y%m%d')
            unique_part = uuid.uuid4().hex[:6].upper()
            self.order_number = f"ACD-{date_str}-{unique_part}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.order_number} - {self.customer_name} (₦{self.total_amount:,.2f})"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL)
    product_name = models.CharField(max_length=200)
    variation_name = models.CharField(max_length=100, blank=True)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)

    def save(self, *args, **kwargs):
        self.subtotal = self.unit_price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity}x {self.product_name} in {self.order.order_number}"
