import uuid
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class CustomCakeEnquiry(models.Model):
    OCCASION_CHOICES = [
        ('birthday', 'Birthday Celebration'),
        ('wedding', 'Wedding / Engagement'),
        ('anniversary', 'Anniversary'),
        ('graduation', 'Graduation'),
        ('baby_shower', 'Baby Shower / Gender Reveal'),
        ('corporate', 'Corporate Event'),
        ('other', 'Special Celebration (Other)'),
    ]

    SIZE_CHOICES = [
        ('6_inch', '6-inch Round (8–10 servings)'),
        ('8_inch', '8-inch Round (16–20 servings)'),
        ('10_inch', '10-inch Round (25–30 servings)'),
        ('2_tier', '2-Tier Celebration (35–45 servings)'),
        ('3_tier', '3-Tier Luxury Grand (60+ servings)'),
        ('bento', 'Mini Bento Cake (1–2 servings)'),
        ('custom', 'Custom Size / Multi-Tier Inquiry'),
    ]

    FLAVOUR_CHOICES = [
        ('vanilla_bean', 'Madagascar Vanilla Bean & Buttercream'),
        ('rich_chocolate', 'Rich Belgian Chocolate Fudge'),
        ('red_velvet', 'Signature Red Velvet with Cream Cheese'),
        ('caramel_biscoff', 'Salted Caramel & Lotus Biscoff'),
        ('lemon_blueberry', 'Zesty Lemon & Blueberry Compote'),
        ('strawberry_cream', 'Fresh Strawberries & Whipped Cream'),
        ('cookies_cream', 'Cookies & Cream Oreo Delight'),
        ('custom_combo', 'Custom Flavour Combination'),
    ]

    FULFILMENT_CHOICES = [
        ('pickup', 'Self-Pickup at Bakery'),
        ('delivery', 'Doorstep Delivery'),
    ]

    BUDGET_CHOICES = [
        ('25k_40k', '₦25,000 – ₦40,000'),
        ('40k_70k', '₦40,000 – ₦70,000'),
        ('70k_120k', '₦70,000 – ₦120,000'),
        ('120k_plus', '₦120,000+ (Luxury Custom Design)'),
        ('flexible', 'Flexible / Dependent on Quote'),
    ]

    STATUS_CHOICES = [
        ('new', 'New Request'),
        ('under_review', 'Under Review'),
        ('quoted', 'Quote Provided'),
        ('confirmed', 'Order Confirmed'),
        ('completed', 'Completed'),
        ('declined', 'Declined / Unavailable'),
    ]

    reference_number = models.CharField(max_length=20, unique=True, editable=False)
    customer_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30, help_text="Phone or WhatsApp number for quick contact")
    occasion = models.CharField(max_length=50, choices=OCCASION_CHOICES, default='birthday')
    cake_size = models.CharField(max_length=50, choices=SIZE_CHOICES, default='8_inch')
    flavour = models.CharField(max_length=50, choices=FLAVOUR_CHOICES, default='rich_chocolate')
    design_description = models.TextField(help_text="Describe color scheme, theme, wording on cake, design style")
    reference_image = models.ImageField(upload_to='cakes/references/', blank=True, null=True, help_text="Optional photo reference or sketch")
    requested_date = models.DateField(help_text="Date needed for delivery or pickup")
    fulfilment_option = models.CharField(max_length=20, choices=FULFILMENT_CHOICES, default='pickup')
    delivery_address = models.TextField(blank=True, help_text="Delivery address if delivery selected")
    budget_range = models.CharField(max_length=50, choices=BUDGET_CHOICES, default='40k_70k')
    additional_notes = models.TextField(blank=True)
    
    # Staff / Admin fields
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='new')
    quoted_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    internal_notes = models.TextField(blank=True, help_text="Internal notes for bakery staff")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Custom Cake Enquiries"

    def save(self, *args, **kwargs):
        if not self.reference_number:
            self.reference_number = f"ACK-{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.reference_number} - {self.customer_name} ({self.get_occasion_display()})"


class SurprisePackage(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    short_description = models.CharField(max_length=300)
    full_description = models.TextField()
    starting_price = models.DecimalField(max_digits=12, decimal_places=2, help_text="Starting price in ₦")
    image = models.ImageField(upload_to='packages/', blank=True, null=True)
    included_items = models.TextField(help_text="Items included, one per line")
    occasions = models.ManyToManyField('catalog.Occasion', blank=True, related_name='surprise_packages')
    lead_time_hours = models.PositiveIntegerField(default=24)
    is_customizable = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['display_order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('enquiries:package_detail', kwargs={'slug': self.slug})

    def get_items_list(self):
        if not self.included_items:
            return []
        return [item.strip() for item in self.included_items.split('\n') if item.strip()]


class SurprisePackageEnquiry(models.Model):
    STATUS_CHOICES = [
        ('new', 'New Request'),
        ('reviewing', 'In Discussion'),
        ('confirmed', 'Confirmed & Scheduled'),
        ('fulfilled', 'Delivered & Completed'),
        ('cancelled', 'Cancelled'),
    ]

    reference_number = models.CharField(max_length=20, unique=True, editable=False)
    package = models.ForeignKey(SurprisePackage, on_delete=models.SET_NULL, null=True, blank=True, related_name='enquiries')
    sender_name = models.CharField(max_length=150)
    sender_email = models.EmailField()
    sender_phone = models.CharField(max_length=30)
    recipient_name = models.CharField(max_length=150)
    recipient_phone = models.CharField(max_length=30)
    delivery_address = models.TextField()
    occasion = models.CharField(max_length=100)
    delivery_date = models.DateField()
    personal_card_message = models.TextField(blank=True, help_text="Handwritten greeting card note for the recipient")
    custom_addons = models.CharField(max_length=300, blank=True, help_text="e.g. Extra cupcakes, chocolates, scented candle, customized mug")
    budget_range = models.CharField(max_length=100, blank=True)
    additional_instructions = models.TextField(blank=True)
    
    # Staff / Admin
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='new')
    internal_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Surprise Package Enquiries"

    def save(self, *args, **kwargs):
        if not self.reference_number:
            self.reference_number = f"ASP-{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.reference_number} - For {self.recipient_name} by {self.sender_name}"
