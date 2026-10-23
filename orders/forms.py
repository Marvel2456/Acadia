from django import forms
from .models import Order


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'customer_name',
            'customer_email',
            'customer_phone',
            'fulfilment_type',
            'delivery_address',
            'delivery_city',
            'preferred_date',
            'preferred_time_slot',
            'special_notes',
            'payment_method',
        ]
        widgets = {
            'customer_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-stone-200 focus:outline-none focus:ring-2 focus:ring-[#FFBD55] text-stone-800 text-sm font-medium',
                'placeholder': 'Your Full Name'
            }),
            'customer_email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-stone-200 focus:outline-none focus:ring-2 focus:ring-[#FFBD55] text-stone-800 text-sm font-medium',
                'placeholder': 'name@example.com'
            }),
            'customer_phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-stone-200 focus:outline-none focus:ring-2 focus:ring-[#FFBD55] text-stone-800 text-sm font-medium',
                'placeholder': '0801 234 5678 (or WhatsApp)'
            }),
            'fulfilment_type': forms.RadioSelect(attrs={
                'class': 'text-[#FFBD55] focus:ring-[#FFBD55]'
            }),
            'delivery_address': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-stone-200 focus:outline-none focus:ring-2 focus:ring-[#FFBD55] text-stone-800 text-sm font-medium',
                'rows': 3,
                'placeholder': 'Street address, estate, apartment number, landmark'
            }),
            'delivery_city': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-stone-200 focus:outline-none focus:ring-2 focus:ring-[#FFBD55] text-stone-800 text-sm font-medium',
                'placeholder': 'Lagos (e.g. Lekki, Ikeja, Victoria Island, Yaba)'
            }),
            'preferred_date': forms.DateInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-stone-200 focus:outline-none focus:ring-2 focus:ring-[#FFBD55] text-stone-800 text-sm font-medium',
                'type': 'date'
            }),
            'preferred_time_slot': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-stone-200 focus:outline-none focus:ring-2 focus:ring-[#FFBD55] text-stone-800 text-sm font-medium',
                'placeholder': 'e.g. Morning 10am-1pm or Afternoon 2pm-5pm'
            }),
            'special_notes': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-stone-200 focus:outline-none focus:ring-2 focus:ring-[#FFBD55] text-stone-800 text-sm font-medium',
                'rows': 2,
                'placeholder': 'Allergies, birthday greeting on cake box, gate code, or delivery instructions'
            }),
            'payment_method': forms.RadioSelect(attrs={
                'class': 'text-[#FFBD55] focus:ring-[#FFBD55]'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        fulfilment_type = cleaned_data.get('fulfilment_type')
        delivery_address = cleaned_data.get('delivery_address')

        if fulfilment_type == 'delivery' and not delivery_address:
            self.add_error('delivery_address', 'Delivery address is required for doorstep delivery.')

        return cleaned_data
