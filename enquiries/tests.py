import datetime
from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from enquiries.models import CustomCakeEnquiry, SurprisePackage
from cms.models import SiteSettings


class EnquiriesTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.settings = SiteSettings.objects.create(id=1, lead_time_cake_days=2)
        self.package = SurprisePackage.objects.create(
            name="Milestone Surprise Box",
            slug="milestone-surprise-box",
            starting_price=Decimal("45000.00"),
            short_description="A lovely package",
            full_description="Detailed info",
            is_available=True
        )

    def test_custom_cake_page_loads(self):
        res = self.client.get(reverse('enquiries:custom_cake'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Your Dream Cake")

    def test_custom_cake_enquiry_submission(self):
        valid_date = timezone.localdate() + datetime.timedelta(days=4)
        post_data = {
            'customer_name': 'Chidi Benson',
            'email': 'chidi@example.com',
            'phone': '08123456789',
            'occasion': 'birthday',
            'cake_size': '8_inch',
            'flavour': 'red_velvet',
            'design_description': 'Pastel gold celebration theme with buttercream florals',
            'requested_date': valid_date.strftime('%Y-%m-%d'),
            'fulfilment_option': 'pickup',
            'budget_range': '40k_70k',
        }
        res = self.client.post(reverse('enquiries:custom_cake'), post_data)
        self.assertEqual(res.status_code, 302)
        self.assertTrue(CustomCakeEnquiry.objects.filter(customer_name='Chidi Benson').exists())

    def test_surprise_packages_page(self):
        res = self.client.get(reverse('enquiries:surprise_packages'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Milestone Surprise Box")
        self.assertContains(res, "45,000")
