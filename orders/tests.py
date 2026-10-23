from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from catalog.models import Category, Product, ProductVariation
from orders.models import Order, OrderItem
from cms.models import SiteSettings


class OrdersTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.settings = SiteSettings.objects.create(
            id=1,
            standard_delivery_fee=Decimal('2500.00'),
            free_delivery_threshold=Decimal('50000.00')
        )
        self.category = Category.objects.create(name="Cakes", slug="cakes")
        self.product = Product.objects.create(
            name="Vanilla Dream Cake",
            slug="vanilla-dream-cake",
            category=self.category,
            price=Decimal("20000.00"),
            short_description="Moist vanilla sponge",
            is_available=True
        )

    def test_cart_add_and_detail(self):
        # Add to cart
        res = self.client.post(
            reverse('orders:cart_add', kwargs={'product_id': self.product.id}),
            {'quantity': 2},
            HTTP_HX_REQUEST="true"
        )
        self.assertEqual(res.status_code, 200)

        # Check cart detail page
        detail_res = self.client.get(reverse('orders:cart_detail'))
        self.assertEqual(detail_res.status_code, 200)
        self.assertContains(detail_res, "Vanilla Dream Cake")
        self.assertContains(detail_res, "40,000")

    def test_checkout_submission(self):
        # Add item to cart first
        self.client.post(reverse('orders:cart_add', kwargs={'product_id': self.product.id}), {'quantity': 1})
        
        # Submit checkout
        post_data = {
            'customer_name': 'Amara Okonkwo',
            'customer_email': 'amara@example.com',
            'customer_phone': '08099887766',
            'fulfilment_type': 'delivery',
            'delivery_address': '12 Victoria Island',
            'delivery_city': 'Lagos',
            'payment_method': 'bank_transfer',
        }
        res = self.client.post(reverse('orders:checkout'), post_data)
        self.assertEqual(res.status_code, 302)

        # Verify Order created in DB
        order = Order.objects.get(customer_name='Amara Okonkwo')
        self.assertEqual(order.subtotal_amount, Decimal('20000.00'))
        self.assertEqual(order.delivery_fee, Decimal('2500.00'))
        self.assertEqual(order.total_amount, Decimal('22500.00'))
        self.assertEqual(order.items.count(), 1)
        self.assertEqual(order.items.first().product_name, "Vanilla Dream Cake")
