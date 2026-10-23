from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from .models import Category, Occasion, Product, ProductVariation


class CatalogTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name="Pastries", slug="pastries")
        self.occasion = Occasion.objects.create(name="Birthdays", slug="birthdays")
        self.product = Product.objects.create(
            name="Butter Croissant",
            slug="butter-croissant",
            category=self.category,
            price=Decimal("2500.00"),
            short_description="Flaky French croissant",
            is_available=True,
            is_bestseller=True
        )
        self.product.occasions.add(self.occasion)
        self.variation = ProductVariation.objects.create(
            product=self.product,
            name="Box of 4",
            price_modifier=Decimal("7000.00"),
            is_available=True
        )

    def test_product_list_view(self):
        response = self.client.get(reverse('catalog:product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Butter Croissant")
        self.assertContains(response, "₦2,500")

    def test_category_filter(self):
        response = self.client.get(f"{reverse('catalog:product_list')}?category=pastries")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Butter Croissant")

    def test_htmx_search(self):
        response = self.client.get(
            f"{reverse('catalog:product_list')}?q=Croissant",
            HTTP_HX_REQUEST="true"
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Butter Croissant")

    def test_product_detail_view(self):
        response = self.client.get(reverse('catalog:product_detail', kwargs={'slug': 'butter-croissant'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Butter Croissant")
        self.assertContains(response, "Box of 4")
