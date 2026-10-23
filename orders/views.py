from decimal import Decimal
import json
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db import transaction
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from catalog.models import Product, ProductVariation
from cms.models import SiteSettings
from .cart import Cart
from .models import Order, OrderItem
from .forms import CheckoutForm


def cart_detail(request):
    cart = Cart(request)
    context = {
        'cart': cart,
    }
    return render(request, 'orders/cart.html', context)


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id, is_available=True)
    variation_id = request.POST.get('variation')
    quantity = int(request.POST.get('quantity', 1))

    variation = None
    if variation_id:
        try:
            variation = ProductVariation.objects.get(id=int(variation_id), product=product, is_available=True)
        except (ProductVariation.DoesNotExist, ValueError):
            variation = None

    cart.add(product=product, variation=variation, quantity=quantity)

    # Return HTMX response with updated cart badge & optional notification toast
    if request.headers.get('HX-Request'):
        response = render(request, 'partials/cart_badge.html', {
            'cart': cart,
            'cart_count': len(cart),
            'cart_subtotal': cart.get_subtotal(),
            'just_added_name': product.name,
        })
        response['HX-Trigger'] = json.dumps({
            'cartUpdated': {'count': len(cart), 'subtotal': str(cart.get_subtotal()), 'name': product.name}
        })
        return response

    messages.success(request, f"Added {product.name} to your cart!")
    return redirect('orders:cart_detail')


@require_POST
def cart_update_quantity(request, key):
    cart = Cart(request)
    action = request.POST.get('action')
    try:
        current_qty = cart.cart.get(key, {}).get('quantity', 1)
        if action == 'increase':
            new_qty = current_qty + 1
        elif action == 'decrease':
            new_qty = max(0, current_qty - 1)
        else:
            new_qty = int(request.POST.get('quantity', 1))
        
        cart.update_quantity(key, new_qty)
    except Exception:
        pass

    if request.headers.get('HX-Request'):
        response = render(request, 'orders/partials/cart_table.html', {'cart': cart})
        response['HX-Trigger'] = json.dumps({
            'cartUpdated': {'count': len(cart), 'subtotal': str(cart.get_subtotal())}
        })
        return response

    return redirect('orders:cart_detail')


@require_POST
def cart_remove(request, key):
    cart = Cart(request)
    cart.remove(key)

    if request.headers.get('HX-Request'):
        response = render(request, 'orders/partials/cart_table.html', {'cart': cart})
        response['HX-Trigger'] = json.dumps({
            'cartUpdated': {'count': len(cart), 'subtotal': str(cart.get_subtotal())}
        })
        return response

    return redirect('orders:cart_detail')


def cart_drawer(request):
    cart = Cart(request)
    return render(request, 'partials/cart_drawer.html', {'cart': cart})


def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, "Your cart is empty. Add delicious treats before checkout!")
        return redirect('catalog:product_list')

    site_settings = SiteSettings.get_settings()

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                order = form.save(commit=False)
                
                # Calculate financial fields securely on server
                subtotal = cart.get_subtotal()
                delivery_fee = cart.get_delivery_fee(order.fulfilment_type)
                total = subtotal + delivery_fee
                
                order.subtotal_amount = subtotal
                order.delivery_fee = delivery_fee
                order.total_amount = total
                order.payment_status = 'pending'
                order.fulfilment_status = 'pending'
                order.save()

                # Snapshot Order Items
                for item in cart:
                    OrderItem.objects.create(
                        order=order,
                        product=item['product'],
                        product_name=item['product'].name,
                        variation_name=item['variation'].name if item['variation'] else '',
                        unit_price=item['unit_price'],
                        quantity=item['quantity'],
                        subtotal=item['total_price']
                    )

                # Clear session cart
                cart.clear()

                # If Paystack is chosen and secret key is configured, initialize server-side
                if order.payment_method == 'paystack' and site_settings.paystack_secret_key:
                    paystack_url = initialize_paystack_payment(request, order, site_settings)
                    if paystack_url:
                        return redirect(paystack_url)

                messages.success(request, f"Order {order.order_number} placed successfully!")
                return redirect('orders:order_confirmation', order_number=order.order_number)
    else:
        form = CheckoutForm(initial={
            'fulfilment_type': 'delivery',
            'delivery_city': 'Lagos',
            'payment_method': 'bank_transfer',
        })

    context = {
        'cart': cart,
        'form': form,
        'site_settings': site_settings,
        'standard_fee': site_settings.standard_delivery_fee,
        'free_threshold': site_settings.free_delivery_threshold,
    }
    return render(request, 'orders/checkout.html', context)


def order_confirmation(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    site_settings = SiteSettings.get_settings()
    context = {
        'order': order,
        'site_settings': site_settings,
    }
    return render(request, 'orders/order_confirmation.html', context)


def initialize_paystack_payment(request, order, site_settings):
    """
    Server-side Paystack payment initialization.
    Secures API credentials and validates order amount strictly on server.
    """
    secret_key = site_settings.paystack_secret_key or settings.PAYSTACK_SECRET_KEY
    if not secret_key:
        return None

    url = "https://api.paystack.co/transaction/initialize"
    headers = {
        "Authorization": f"Bearer {secret_key}",
        "Content-Type": "application/json",
    }
    callback_url = request.build_absolute_uri(reverse('orders:verify_payment'))
    amount_kobo = int(order.total_amount * 100)

    payload = {
        "email": order.customer_email,
        "amount": amount_kobo,
        "reference": order.order_number,
        "callback_url": callback_url,
        "metadata": {
            "order_number": order.order_number,
            "customer_name": order.customer_name,
            "phone": order.customer_phone,
        }
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        data = response.json()
        if data.get('status') and data.get('data', {}).get('authorization_url'):
            order.paystack_reference = order.order_number
            order.save(update_fields=['paystack_reference'])
            return data['data']['authorization_url']
    except Exception:
        pass
    return None


def verify_payment(request):
    """
    Paystack callback verification.
    Validates payment status against Paystack API before updating order status.
    """
    reference = request.GET.get('reference') or request.GET.get('trxref')
    if not reference:
        messages.error(request, "No transaction reference provided.")
        return redirect('catalog:product_list')

    order = get_object_or_404(Order, order_number=reference)
    site_settings = SiteSettings.get_settings()
    secret_key = site_settings.paystack_secret_key or settings.PAYSTACK_SECRET_KEY

    if secret_key:
        url = f"https://api.paystack.co/transaction/verify/{reference}"
        headers = {"Authorization": f"Bearer {secret_key}"}
        try:
            res = requests.get(url, headers=headers, timeout=10)
            data = res.json()
            if data.get('status') and data.get('data', {}).get('status') == 'success':
                paid_amount = Decimal(data['data']['amount']) / 100
                if paid_amount >= order.total_amount:
                    order.payment_status = 'paid'
                    order.fulfilment_status = 'confirmed'
                    order.paystack_reference = reference
                    order.save(update_fields=['payment_status', 'fulfilment_status', 'paystack_reference'])
                    messages.success(request, f"Payment confirmed! Thank you for your order.")
                else:
                    order.payment_status = 'failed'
                    order.internal_notes += f"\nWarning: Paid amount ₦{paid_amount} differs from total ₦{order.total_amount}"
                    order.save(update_fields=['payment_status', 'internal_notes'])
            else:
                order.payment_status = 'failed'
                order.save(update_fields=['payment_status'])
                messages.error(request, "Payment verification was unsuccessful.")
        except Exception:
            messages.warning(request, "Could not verify payment automatically. Staff will verify manual payment.")

    return redirect('orders:order_confirmation', order_number=order.order_number)
