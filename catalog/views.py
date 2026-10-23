from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Category, Occasion, Product, ProductVariation


def product_list(request):
    category_slug = request.GET.get('category')
    occasion_slug = request.GET.get('occasion')
    query = request.GET.get('q', '').strip()
    sort = request.GET.get('sort', 'order')

    products = Product.objects.filter(is_available=True)
    active_category = None
    active_occasion = None

    if category_slug:
        active_category = get_object_or_404(Category, slug=category_slug, is_active=True)
        products = products.filter(category=active_category)

    if occasion_slug:
        active_occasion = get_object_or_404(Occasion, slug=occasion_slug, is_active=True)
        products = products.filter(occasions=active_occasion)

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(short_description__icontains=query) |
            Q(full_description__icontains=query)
        )

    if sort == 'price_low':
        products = products.order_by('price')
    elif sort == 'price_high':
        products = products.order_by('-price')
    elif sort == 'newest':
        products = products.order_by('-created_at')
    else:
        products = products.order_by('display_order', '-is_bestseller', 'name')

    categories = Category.objects.filter(is_active=True).order_by('display_order', 'name')
    occasions = Occasion.objects.filter(is_active=True).order_by('display_order', 'name')

    context = {
        'products': products,
        'categories': categories,
        'occasions': occasions,
        'active_category': active_category,
        'active_occasion': active_occasion,
        'query': query,
        'sort': sort,
        'total_count': products.count(),
    }

    # If requested by HTMX for live filter/search, return the partial product grid
    if request.headers.get('HX-Request') and not request.headers.get('HX-Target') == 'main-content':
        return render(request, 'catalog/partials/product_grid.html', context)

    return render(request, 'catalog/product_list.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_available=True)
    variations = product.variations.filter(is_available=True)
    related_products = Product.objects.filter(category=product.category, is_available=True).exclude(id=product.id)[:4]

    context = {
        'product': product,
        'variations': variations,
        'related_products': related_products,
    }
    return render(request, 'catalog/product_detail.html', context)
