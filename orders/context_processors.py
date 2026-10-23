from .cart import Cart


def cart_summary(request):
    try:
        cart = Cart(request)
        return {
            'cart': cart,
            'cart_count': len(cart),
            'cart_subtotal': cart.get_subtotal(),
        }
    except Exception:
        return {
            'cart': None,
            'cart_count': 0,
            'cart_subtotal': 0,
        }
