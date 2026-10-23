import datetime
from django import forms
from django.utils import timezone
from cms.models import SiteSettings
from .models import CustomCakeEnquiry, SurprisePackageEnquiry, SurprisePackage


class CustomCakeEnquiryForm(forms.ModelForm):
    class Meta:
        model = CustomCakeEnquiry
        fields = [
            'customer_name',
            'email',
            'phone',
            'occasion',
            'cake_size',
            'flavour',
            'design_description',
            'reference_image',
            'requested_date',
            'fulfilment_option',
            'delivery_address',
            'budget_range',
            'additional_notes',
        ]
        widgets = {
            'customer_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-stone-200 focus:outline-none focus:ring-2 focus:ring-[#FFBD55] text-stone-800 text-sm font-medium',
                'placeholder': 'Your Full Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-stone-200 focus:outline-none focus:ring-2 focus:ring-[#FFBD55] text-stone-800 text-sm font-medium',
                'placeholder': 'your.email@example.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-stone-200 focus:outline-none focus:ring-2 focus:ring-[#FFBD55] text-stone-800 text-sm font-medium',
                'placeholder': 'Phone or WhatsApp Number'
            }),
            'occasion': forms.Select(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-stone-200 focus:outline-none focus:ring-2 focus:ring-[#FFBD55] text-stone-800 text-sm font-medium bg-white'
            }),
            'cake_size': forms.Select(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-stone-200 focus:outline-none focus:ring-2 focus:ring-[#FFBD55] text-stone-800 text-sm font-medium bg-white'
            }),
            'flavour': forms.Select(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-stone-200 focus:outline-none focus:ring-2 focus:ring-[#FFBD55] text-stone-800 text-sm font-medium bg-white'
            }),
            'design_description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-stone-200 focus:outline-none focus:ring-2 focus:ring-[#FFBD55] text-stone-800 text-sm font-medium',
                'rows': 4,
                'placeholder': 'Describe your dream theme, color scheme, wording to pipe on the cake, or specific design accents...'
            }),
            'reference_image': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-dashed border-stone-300 bg-stone-50 text-stone-700 text-sm file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-[#FFBD55] file:text-stone-900 hover:file:bg-[#fcae33]'
            }),
            'requested_date': forms.DateInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-stone-200 focus:outline-none focus:ring-2 focus:ring-[#FFBD55] text-stone-800 text-sm font-medium',
                'type': 'date'
            }),
            'fulfilment_option': forms.Select(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-stone-200 focus:outline-none focus:ring-2 focus:ring-[#FFBD55] text-stone-800 text-sm font-medium bg-white'
            }),
            'delivery_address': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-stone-200 focus:outline-none focus:ring-2 focus:ring-[#FFBD55] text-stone-800 text-sm font-medium',
                'rows': 2,
                'placeholder': 'Delivery address in Lagos (leave blank if selecting self-pickup)'
            }),
            'budget_range': forms.Select(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-stone-200 focus:outline-none focus:ring-2 focus:ring-[#FFBD55] text-stone-800 text-sm font-medium bg-white'
            }),
            'additional_notes': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-stone-200 focus:outline-none focus:ring-2 focus:ring-[#FFBD55] text-stone-800 text-sm font-medium',
                'rows': 2,
                'placeholder': 'Dietary requirements, preferred pickup/delivery time, candles, etc.'
            }),
        }

    def clean_requested_date(self):
        req_date = self.cleaned_data.get('requested_date')
        if not req_date:
            return req_date

        today = timezone.localdate()
        if req_date <= today:
            raise forms.ValidationError("Requested date must be in the future.")

        try:
            site_settings = SiteSettings.get_settings()
            lead_days = site_settings.lead_time_cake_days
        except Exception:
            lead_days = 2

        min_date = today + datetime.timedelta(days=lead_days)
        if req_date < min_date:
            raise forms.ValidationError(
                f"Custom cakes require a minimum lead time of {lead_days} days. Earliest available date is {min_date.strftime('%B %d, %Y')}."
            )

        return req_date


class SurprisePackageEnquiryForm(forms.ModelForm):
    class Meta:
        model = SurprisePackageEnquiry
        fields = [
            'package',
            'sender_name',
            'sender_email',
            'sender_phone',
            'recipient_name',
            'recipient_phone',
            'delivery_address',
            'occasion',
            'delivery_date',
            'personal_card_message',
            'custom_addons',
            'budget_range',
            'additional_instructions',
        ]
        widgets = {
            'package': forms.Select(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-stone-200 focus:outline-none focus:ring-2 focus:ring-[#FFBD55] text-stone-800 text-sm font-medium bg-white'
            }),
            'sender_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-stone-200 focus:outline-none focus:ring-2 focus:ring-[#FFBD55] text-stone-800 text-sm font-medium',
                'placeholder': 'Your Full Name'
            }),
            'sender_email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-stone-200 focus:outline-none focus:ring-2 focus:ring-[#FFBD55] text-stone-800 text-sm font-medium',
                'placeholder': 'your.email@example.com'
            }),
            'sender_phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-stone-200 focus:outline-none focus:ring-2 focus:ring-[#FFBD55] text-stone-800 text-sm font-medium',
                'placeholder': 'Your Phone / WhatsApp'
            }),
            'recipient_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-stone-200 focus:outline-none focus:ring-2 focus:ring-[#FFBD55] text-stone-800 text-sm font-medium',
                'placeholder': 'Recipient Name (The Person Being Surprised)'
            }),
            'recipient_phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-stone-200 focus:outline-none focus:ring-2 focus:ring-[#FFBD55] text-stone-800 text-sm font-medium',
                'placeholder': 'Recipient Phone (For Dispatch Call)'
            }),
            'delivery_address': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-stone-200 focus:outline-none focus:ring-2 focus:ring-[#FFBD55] text-stone-800 text-sm font-medium',
                'rows': 3,
                'placeholder': 'Recipient delivery address (home or office location in Lagos)'
            }),
            'occasion': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-stone-200 focus:outline-none focus:ring-2 focus:ring-[#FFBD55] text-stone-800 text-sm font-medium',
                'placeholder': 'e.g. 30th Birthday, Anniversary, Promotion, Just Because'
            }),
            'delivery_date': forms.DateInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-stone-200 focus:outline-none focus:ring-2 focus:ring-[#FFBD55] text-stone-800 text-sm font-medium',
                'type': 'date'
            }),
            'personal_card_message': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-stone-200 focus:outline-none focus:ring-2 focus:ring-[#FFBD55] text-stone-800 text-sm font-medium',
                'rows': 3,
                'placeholder': 'Write your personal heartfelt message to be handwritten in the greeting card...'
            }),
            'custom_addons': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-stone-200 focus:outline-none focus:ring-2 focus:ring-[#FFBD55] text-stone-800 text-sm font-medium',
                'placeholder': 'Optional: Extra cupcakes, fresh flowers, wine, customized mug'
            }),
            'budget_range': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-stone-200 focus:outline-none focus:ring-2 focus:ring-[#FFBD55] text-stone-800 text-sm font-medium',
                'placeholder': 'e.g. ₦65,000 – ₦80,000'
            }),
            'additional_instructions': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-stone-200 focus:outline-none focus:ring-2 focus:ring-[#FFBD55] text-stone-800 text-sm font-medium',
                'rows': 2,
                'placeholder': 'Preferred time window, anonymous surprise delivery, or special instructions'
            }),
        }

    def clean_delivery_date(self):
        delivery_date = self.cleaned_data.get('delivery_date')
        if not delivery_date:
            return delivery_date

        today = timezone.localdate()
        if delivery_date <= today:
            raise forms.ValidationError("Delivery date must be at least 24 hours in the future.")
        return delivery_date
