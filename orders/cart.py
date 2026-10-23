from decimal import Decimal
from django.conf import settings
from catalog.models import Product, ProductVariation


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def _item_key(self, product_id, variation_id=None):
        if variation_id:
            return f"{product_id}_{variation_id}"
        return f"{product_id}_0"

    def add(self, product, variation=None, quantity=1, override_quantity=False):
        product_id = product.id
        variation_id = variation.id if variation else 0
        key = self._item_key(product_id, variation_id)

        if key not in self.cart:
            self.cart[key] = {
                'product_id': product_id,
                'variation_id': variation_id,
                'quantity': 0,
            }

        if override_quantity:
            self.cart[key]['quantity'] = max(1, quantity)
        else:
            self.cart[key]['quantity'] += max(1, quantity)

        self.save()

    def update_quantity(self, key, quantity):
        if key in self.cart:
            if quantity > 0:
                self.cart[key]['quantity'] = quantity
            else:
                del self.cart[key]
            self.save()

    def remove(self, key):
        if key in self.cart:
            del self.cart[key]
            self.save()

    def clear(self):
        self.session[settings.CART_SESSION_ID] = {}
        self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        # Fetch actual products from DB to ensure prices and availability are strictly server-validated
        product_ids = set()
        variation_ids = set()
        for key, item in self.cart.items():
            product_ids.add(item['product_id'])
            if item.get('variation_id') and item['variation_id'] != 0:
                variation_ids.add(item['variation_id'])

        products = {p.id: p for p in Product.objects.filter(id__in=product_ids)}
        variations = {v.id: v for v in ProductVariation.objects.filter(id__in=variation_ids)}

        for key, item in list(self.cart.items()):
            product = products.get(item['product_id'])
            if not product or not product.is_available:
                # Remove stale or discontinued product
                del self.cart[key]
                self.save()
                continue

            variation = variations.get(item['variation_id']) if item['variation_id'] != 0 else None
            unit_price = variation.get_effective_price() if variation else product.price
            total_price = unit_price * item['quantity']

            yield {
                'key': key,
                'product': product,
                'variation': variation,
                'unit_price': unit_price,
                'quantity': item['quantity'],
                'total_price': total_price,
            }

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_subtotal(self):
        subtotal = Decimal('0.00')
        for item in self:
            subtotal += item['total_price']
        return subtotal

    def get_delivery_fee(self, fulfilment_type='delivery'):
        if fulfilment_type != 'delivery':
            return Decimal('0.00')
        
        # Check free delivery threshold from site settings
        from cms.models import SiteSettings
        try:
            site_settings = SiteSettings.get_settings()
            subtotal = self.get_subtotal()
            if subtotal >= site_settings.free_delivery_threshold:
                return Decimal('0.00')
            return site_settings.standard_delivery_fee
        except Exception:
            return Decimal('2500.00')

    def get_total(self, fulfilment_type='delivery'):
        return self.get_subtotal() + self.get_delivery_fee(fulfilment_type)
