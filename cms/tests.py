from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from catalog.models import Category, Product
from cms.models import SiteSettings, HeroSection, NewsletterSubscriber


class CMSTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.site_settings = SiteSettings.get_settings()
        self.site_settings.business_name = "Acadia Bakery & Bistro"
        self.site_settings.save()

        self.category = Category.objects.create(name="Pastries", slug="pastries")
        self.product = Product.objects.create(
            category=self.category,
            name="Butter Croissant",
            slug="butter-croissant",
            price=2500,
            short_description="Golden flaky pastry",
            is_available=True,
            is_bestseller=True
        )

        self.staff_user = User.objects.create_user(
            username='staff',
            password='password123',
            is_staff=True
        )

    def test_home_view(self):
        response = self.client.get(reverse('cms:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Acadia")
        self.assertContains(response, "Butter Croissant")

    def test_about_and_contact_views(self):
        about_resp = self.client.get(reverse('cms:about'))
        self.assertEqual(about_resp.status_code, 200)

        contact_resp = self.client.get(reverse('cms:contact'))
        self.assertEqual(contact_resp.status_code, 200)

    def test_newsletter_subscribe(self):
        # Valid email
        response = self.client.post(
            reverse('cms:newsletter_subscribe'),
            {'email': 'taste@acadia.ng'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(NewsletterSubscriber.objects.filter(email='taste@acadia.ng').exists())

        # Invalid email
        response = self.client.post(
            reverse('cms:newsletter_subscribe'),
            {'email': 'invalid-email'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "valid email")

    def test_robots_txt(self):
        response = self.client.get(reverse('robots_txt'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/plain')
        self.assertIn("User-agent: *", response.content.decode())
        self.assertIn("Sitemap:", response.content.decode())

    def test_sitemap_xml(self):
        response = self.client.get(reverse('sitemap_xml'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/xml')
        self.assertIn("<urlset", response.content.decode())
        self.assertIn("/shop/butter-croissant/", response.content.decode())

    def test_staff_cms_access(self):
        # Unauthenticated staff redirect
        response = self.client.get(reverse('cms:dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('cms:login'), response.url)

        # Authenticated staff access
        self.client.login(username='staff', password='password123')
        auth_response = self.client.get(reverse('cms:dashboard'))
        self.assertEqual(auth_response.status_code, 200)
        self.assertContains(auth_response, "Staff CMS")
