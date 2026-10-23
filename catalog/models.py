from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    icon_name = models.CharField(max_length=50, blank=True, default='cake', help_text="cake, pastry, meal, dessert, gift, celebration")
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['display_order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"{reverse('catalog:product_list')}?category={self.slug}"


class Occasion(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='occasions/', blank=True, null=True)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"{reverse('catalog:product_list')}?occasion={self.slug}"


class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.PROTECT,
        help_text="Products cannot be deleted unintentionally by deleting a category."
    )
    occasions = models.ManyToManyField(Occasion, blank=True, related_name='products')
    short_description = models.CharField(max_length=300, help_text="One or two sentences for cards and previews")
    full_description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, help_text="Price in Nigerian Naira (₦)")
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    is_available = models.BooleanField(default=True, db_index=True)
    is_featured = models.BooleanField(default=False, db_index=True)
    is_bestseller = models.BooleanField(default=False, help_text="Explicitly configured bestseller designation")
    lead_time_hours = models.PositiveIntegerField(default=24, help_text="Standard preparation lead time in hours")
    servings_or_size = models.CharField(max_length=100, blank=True, help_text="e.g. Serves 8-12, or Box of 6")
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog:product_detail', kwargs={'slug': self.slug})


class ProductVariation(models.Model):
    product = models.ForeignKey(Product, related_name='variations', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, help_text="e.g., 8-inch, 10-inch, 12 cupcakes, etc.")
    price_modifier = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Additional cost added to base price")
    is_default = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)

    def get_effective_price(self):
        return self.product.price + self.price_modifier

    def __str__(self):
        if self.price_modifier > 0:
            return f"{self.product.name} - {self.name} (+₦{self.price_modifier:,.2f})"
        return f"{self.product.name} - {self.name}"
