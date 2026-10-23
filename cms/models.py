from django.db import models


class SiteSettings(models.Model):
    LOGO_CHOICES = [
        ('script_character', 'Playful Script Wordmark with Character'),
        ('badge_standard', 'Decorative Badge Logo (Cream & Charcoal)'),
        ('badge_lavender', 'Lavender Badge Variant'),
        ('wordmark_orange', 'Warm Orange Script Wordmark'),
        ('custom_upload', 'Custom Uploaded Logo File'),
    ]

    business_name = models.CharField(max_length=150, default="Acadia")
    tagline = models.CharField(max_length=255, default="A Little Sweetness. A Lot of Love.")
    phone = models.CharField(max_length=50, default="+234 812 345 6789")
    whatsapp_number = models.CharField(max_length=50, default="2348123456789", help_text="Digits only with country code, e.g. 2348123456789")
    email = models.EmailField(default="orders@acadiabakes.com")
    address = models.CharField(max_length=255, default="Plot 12 Admiralty Way, Lekki Phase 1, Lagos, Nigeria")
    opening_hours = models.CharField(max_length=200, default="Mon – Sat: 8:00 AM – 8:00 PM | Sun: 11:00 AM – 6:00 PM")
    
    # Logo selection
    active_logo = models.CharField(max_length=50, choices=LOGO_CHOICES, default='script_character')
    custom_logo = models.ImageField(upload_to='settings/logos/', blank=True, null=True, help_text="Upload your own logo if 'Custom Uploaded Logo File' is chosen")
    
    # Story preview on homepage
    about_story_short = models.TextField(
        default="At Acadia, we believe that food and celebration are deeply personal. Every morning starts before dawn in our ovens, whipping fresh creams, rolling buttery doughs, and simmering savoury ingredients just right for your taste buds."
    )
    
    # Lead times & Order policies
    lead_time_cake_days = models.PositiveIntegerField(default=2, help_text="Minimum notice required for custom cakes (days)")
    lead_time_packages_hours = models.PositiveIntegerField(default=24, help_text="Minimum notice for surprise packages (hours)")
    standard_delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=2500.00, help_text="Standard Lagos delivery fee (₦)")
    free_delivery_threshold = models.DecimalField(max_digits=12, decimal_places=2, default=60000.00, help_text="Order amount above which delivery is free (₦)")

    # Bank Transfer Details
    bank_name = models.CharField(max_length=100, default="Guaranty Trust Bank (GTB)")
    account_number = models.CharField(max_length=30, default="0123456789")
    account_name = models.CharField(max_length=150, default="Acadia Bakery & Confectionery Ltd")
    allow_bank_transfer = models.BooleanField(default=True)

    # Paystack payment credentials
    allow_paystack = models.BooleanField(default=True)
    paystack_public_key = models.CharField(max_length=150, blank=True, help_text="pk_test_... or pk_live_...")
    paystack_secret_key = models.CharField(max_length=150, blank=True, help_text="sk_test_... or sk_live_...")

    # Social links
    instagram_url = models.CharField(max_length=200, blank=True, default="https://instagram.com/acadia_bakes")
    tiktok_url = models.CharField(max_length=200, blank=True, default="https://tiktok.com/@acadia_bakes")
    facebook_url = models.CharField(max_length=200, blank=True, default="https://facebook.com/acadiabakes")
    
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return f"{self.business_name} Site Configuration"

    @classmethod
    def get_settings(cls):
        obj, _ = cls.objects.get_or_create(id=1)
        return obj

    def get_active_logo_url(self):
        if self.active_logo == 'custom_upload' and self.custom_logo:
            return self.custom_logo.url
        elif self.active_logo == 'badge_standard':
            return '/static/images/logos/acadia-badge.svg'
        elif self.active_logo == 'badge_lavender':
            return '/static/images/logos/acadia-badge-lavender.svg'
        elif self.active_logo == 'wordmark_orange':
            return '/static/images/logos/acadia-wordmark-orange.svg'
        # Default
        return '/static/images/logos/acadia-script-character.svg'


class HeroSection(models.Model):
    headline = models.CharField(max_length=200, default="A Little Sweetness. A Lot of Love.")
    subheadline = models.TextField(
        default="From freshly baked treats and delicious meals to beautiful celebration cakes and thoughtful surprise packages, Acadia makes every moment taste special."
    )
    badge_text = models.CharField(max_length=100, default="Handcrafted Fresh Daily in Lagos")
    primary_cta_text = models.CharField(max_length=60, default="Explore Our Menu")
    primary_cta_url = models.CharField(max_length=100, default="/shop/")
    secondary_cta_text = models.CharField(max_length=60, default="Order a Custom Cake")
    secondary_cta_url = models.CharField(max_length=100, default="/custom-cakes/")
    hero_image = models.ImageField(upload_to='cms/hero/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Homepage Hero Section"

    def __str__(self):
        return self.headline


class PromotionalBanner(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    button_text = models.CharField(max_length=60, default="Shop Now")
    button_url = models.CharField(max_length=100, default="/shop/")
    bg_style = models.CharField(
        max_length=30,
        choices=[('lime', 'Soft Lime (#E0E77A)'), ('lavender', 'Lavender (#E8A9EF)'), ('orange', 'Warm Orange (#FFBD55)')],
        default='lime'
    )
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    customer_name = models.CharField(max_length=100)
    customer_role_or_occasion = models.CharField(max_length=150, help_text="e.g. Birthday Celebration, Wedding Anniversary")
    review_text = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)
    avatar = models.ImageField(upload_to='cms/testimonials/', blank=True, null=True)
    # Critical requirement from prompt: "Display genuine customer reviews only if they exist.
    # If reviews are not available, omit the section or provide a CMS-managed section that remains hidden until authentic reviews are added."
    is_active = models.BooleanField(default=False, help_text="Set to True only once authentic customer review is confirmed")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.customer_name} ({self.customer_role_or_occasion})"


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
