from django import forms
from .models import SiteSettings, HeroSection, PromotionalBanner, Testimonial
from catalog.models import Product, Category, ProductVariation
from orders.models import Order
from enquiries.models import CustomCakeEnquiry, SurprisePackage


class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = [
            'business_name',
            'tagline',
            'phone',
            'whatsapp_number',
            'email',
            'address',
            'opening_hours',
            'active_logo',
            'custom_logo',
            'about_story_short',
            'lead_time_cake_days',
            'lead_time_packages_hours',
            'standard_delivery_fee',
            'free_delivery_threshold',
            'bank_name',
            'account_number',
            'account_name',
            'allow_bank_transfer',
            'allow_paystack',
            'paystack_public_key',
            'paystack_secret_key',
            'instagram_url',
            'tiktok_url',
            'facebook_url',
        ]
        widgets = {
            'business_name': forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 rounded-xl border border-stone-200 text-sm'}),
            'tagline': forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 rounded-xl border border-stone-200 text-sm'}),
            'phone': forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 rounded-xl border border-stone-200 text-sm'}),
            'whatsapp_number': forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 rounded-xl border border-stone-200 text-sm'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-4 py-2.5 rounded-xl border border-stone-200 text-sm'}),
            'address': forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 rounded-xl border border-stone-200 text-sm'}),
            'opening_hours': forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 rounded-xl border border-stone-200 text-sm'}),
            'active_logo': forms.Select(attrs={'class': 'w-full px-4 py-2.5 rounded-xl border border-stone-200 text-sm bg-white'}),
            'about_story_short': forms.Textarea(attrs={'class': 'w-full px-4 py-2.5 rounded-xl border border-stone-200 text-sm', 'rows': 3}),
            'bank_name': forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 rounded-xl border border-stone-200 text-sm'}),
            'account_number': forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 rounded-xl border border-stone-200 text-sm'}),
            'account_name': forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 rounded-xl border border-stone-200 text-sm'}),
            'paystack_public_key': forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 rounded-xl border border-stone-200 text-sm'}),
            'paystack_secret_key': forms.PasswordInput(attrs={'class': 'w-full px-4 py-2.5 rounded-xl border border-stone-200 text-sm'}, render_value=True),
        }


class HeroSectionForm(forms.ModelForm):
    class Meta:
        model = HeroSection
        fields = [
            'headline',
            'subheadline',
            'badge_text',
            'primary_cta_text',
            'primary_cta_url',
            'secondary_cta_text',
            'secondary_cta_url',
            'hero_image',
            'is_active',
        ]
        widgets = {
            'headline': forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 rounded-xl border border-stone-200 text-sm'}),
            'subheadline': forms.Textarea(attrs={'class': 'w-full px-4 py-2.5 rounded-xl border border-stone-200 text-sm', 'rows': 3}),
            'badge_text': forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 rounded-xl border border-stone-200 text-sm'}),
            'primary_cta_text': forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 rounded-xl border border-stone-200 text-sm'}),
            'primary_cta_url': forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 rounded-xl border border-stone-200 text-sm'}),
            'secondary_cta_text': forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 rounded-xl border border-stone-200 text-sm'}),
            'secondary_cta_url': forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 rounded-xl border border-stone-200 text-sm'}),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'category',
            'occasions',
            'price',
            'short_description',
            'full_description',
            'image',
            'is_available',
            'is_featured',
            'is_bestseller',
            'lead_time_hours',
            'servings_or_size',
            'display_order',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 rounded-xl border border-stone-200 text-sm'}),
            'category': forms.Select(attrs={'class': 'w-full px-4 py-2.5 rounded-xl border border-stone-200 text-sm bg-white'}),
            'occasions': forms.SelectMultiple(attrs={'class': 'w-full px-4 py-2.5 rounded-xl border border-stone-200 text-sm'}),
            'price': forms.NumberInput(attrs={'class': 'w-full px-4 py-2.5 rounded-xl border border-stone-200 text-sm'}),
            'short_description': forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 rounded-xl border border-stone-200 text-sm'}),
            'full_description': forms.Textarea(attrs={'class': 'w-full px-4 py-2.5 rounded-xl border border-stone-200 text-sm', 'rows': 4}),
            'servings_or_size': forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 rounded-xl border border-stone-200 text-sm'}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'image', 'icon_name', 'display_order', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 rounded-xl border border-stone-200 text-sm'}),
            'description': forms.Textarea(attrs={'class': 'w-full px-4 py-2.5 rounded-xl border border-stone-200 text-sm', 'rows': 3}),
            'icon_name': forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 rounded-xl border border-stone-200 text-sm'}),
        }


class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['fulfilment_status', 'payment_status', 'internal_notes']
        widgets = {
            'fulfilment_status': forms.Select(attrs={'class': 'w-full px-4 py-2.5 rounded-xl border border-stone-200 text-sm bg-white'}),
            'payment_status': forms.Select(attrs={'class': 'w-full px-4 py-2.5 rounded-xl border border-stone-200 text-sm bg-white'}),
            'internal_notes': forms.Textarea(attrs={'class': 'w-full px-4 py-2.5 rounded-xl border border-stone-200 text-sm', 'rows': 3}),
        }


class CakeEnquiryStatusForm(forms.ModelForm):
    class Meta:
        model = CustomCakeEnquiry
        fields = ['status', 'quoted_price', 'internal_notes']
        widgets = {
            'status': forms.Select(attrs={'class': 'w-full px-4 py-2.5 rounded-xl border border-stone-200 text-sm bg-white'}),
            'quoted_price': forms.NumberInput(attrs={'class': 'w-full px-4 py-2.5 rounded-xl border border-stone-200 text-sm'}),
            'internal_notes': forms.Textarea(attrs={'class': 'w-full px-4 py-2.5 rounded-xl border border-stone-200 text-sm', 'rows': 3}),
        }
