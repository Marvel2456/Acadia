from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count, Q, Sum
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from catalog.models import Category, Occasion, Product, ProductVariation
from orders.models import Order, OrderItem
from enquiries.models import CustomCakeEnquiry, SurprisePackage, SurprisePackageEnquiry
from .models import SiteSettings, HeroSection, PromotionalBanner, Testimonial, NewsletterSubscriber
from .forms import SiteSettingsForm, HeroSectionForm, ProductForm, CategoryForm, OrderStatusForm, CakeEnquiryStatusForm


# ==========================================
# PUBLIC VIEWS
# ==========================================

def home(request):
    site_settings = SiteSettings.get_settings()
    hero = HeroSection.objects.filter(is_active=True).first()
    banner = PromotionalBanner.objects.filter(is_active=True).first()

    categories = Category.objects.filter(is_active=True).order_by('display_order', 'name')
    bestsellers = Product.objects.filter(is_available=True, is_bestseller=True).order_by('display_order', 'name')[:6]
    surprise_packages = SurprisePackage.objects.filter(is_available=True, is_featured=True).order_by('display_order')[:3]
    occasions = Occasion.objects.filter(is_active=True).order_by('display_order', 'name')[:6]
    
    # Requirement: "Display genuine customer reviews only if they exist.
    # If reviews are not available, omit the section or provide a CMS-managed section that remains hidden until authentic reviews are added."
    testimonials = Testimonial.objects.filter(is_active=True).order_by('-created_at')[:3]

    context = {
        'site_settings': site_settings,
        'hero': hero,
        'banner': banner,
        'categories': categories,
        'bestsellers': bestsellers,
        'surprise_packages': surprise_packages,
        'occasions': occasions,
        'testimonials': testimonials,
        'has_testimonials': testimonials.exists(),
    }
    return render(request, 'cms/home.html', context)


def about(request):
    site_settings = SiteSettings.get_settings()
    return render(request, 'cms/about.html', {'site_settings': site_settings})


def contact(request):
    site_settings = SiteSettings.get_settings()
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()

        if name and email and message:
            messages.success(request, f"Thank you, {name}! Your message has been sent to the Acadia team.")
            if request.headers.get('HX-Request'):
                return render(request, 'cms/partials/contact_success.html', {'name': name})
            return redirect('cms:contact')
        else:
            messages.error(request, "Please fill in all required fields.")

    return render(request, 'cms/contact.html', {'site_settings': site_settings})


@require_POST
def newsletter_subscribe(request):
    email = request.POST.get('email', '').strip().lower()
    if not email or '@' not in email:
        return HttpResponse(
            '<div class="text-rose-600 text-xs font-semibold mt-2">Please enter a valid email address.</div>'
        )

    sub, created = NewsletterSubscriber.objects.get_or_create(email=email)
    if created:
        return HttpResponse(
            '<div class="text-emerald-700 text-xs font-bold mt-2">✨ Welcome to Acadia! Check your inbox soon for sweet updates.</div>'
        )
    else:
        return HttpResponse(
            '<div class="text-stone-600 text-xs font-medium mt-2">You are already subscribed to Acadia updates!</div>'
        )


# ==========================================
# STAFF CMS / DASHBOARD VIEWS
# ==========================================

def staff_check(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)


def cms_login_view(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('cms:dashboard')

    error_msg = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user and (user.is_staff or user.is_superuser):
            login(request, user)
            messages.success(request, f"Welcome back, {user.get_full_name() or user.username}!")
            return redirect('cms:dashboard')
        else:
            error_msg = "Invalid staff credentials or insufficient administrative permissions."

    return render(request, 'cms/admin/login.html', {'error_msg': error_msg})


def cms_logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out of Acadia Staff CMS.")
    return redirect('cms:login')


@user_passes_test(staff_check, login_url='/cms/login/')
def cms_dashboard(request):
    total_products = Product.objects.count()
    active_products = Product.objects.filter(is_available=True).count()
    total_categories = Category.objects.count()
    
    pending_orders = Order.objects.filter(fulfilment_status='pending').count()
    preparing_orders = Order.objects.filter(fulfilment_status='preparing').count()
    completed_orders = Order.objects.filter(fulfilment_status='completed').count()
    
    new_cake_enquiries = CustomCakeEnquiry.objects.filter(status='new').count()
    new_surprise_enquiries = SurprisePackageEnquiry.objects.filter(status='new').count()
    
    recent_orders = Order.objects.all().order_by('-created_at')[:8]
    recent_cake_enquiries = CustomCakeEnquiry.objects.all().order_by('-created_at')[:5]

    total_sales = Order.objects.filter(payment_status='paid').aggregate(total=Sum('total_amount'))['total'] or 0

    context = {
        'total_products': total_products,
        'active_products': active_products,
        'total_categories': total_categories,
        'pending_orders': pending_orders,
        'preparing_orders': preparing_orders,
        'completed_orders': completed_orders,
        'new_cake_enquiries': new_cake_enquiries,
        'new_surprise_enquiries': new_surprise_enquiries,
        'recent_orders': recent_orders,
        'recent_cake_enquiries': recent_cake_enquiries,
        'total_sales': total_sales,
    }
    return render(request, 'cms/admin/dashboard.html', context)


@user_passes_test(staff_check, login_url='/cms/login/')
def cms_orders(request):
    status_filter = request.GET.get('status')
    payment_filter = request.GET.get('payment')
    query = request.GET.get('q', '').strip()

    orders = Order.objects.all()

    if status_filter:
        orders = orders.filter(fulfilment_status=status_filter)
    if payment_filter:
        orders = orders.filter(payment_status=payment_filter)
    if query:
        orders = orders.filter(
            Q(order_number__icontains=query) |
            Q(customer_name__icontains=query) |
            Q(customer_email__icontains=query) |
            Q(customer_phone__icontains=query)
        )

    orders = orders.order_by('-created_at')
    
    context = {
        'orders': orders,
        'status_filter': status_filter,
        'payment_filter': payment_filter,
        'query': query,
        'status_choices': Order.FULFILMENT_STATUS_CHOICES,
        'payment_choices': Order.PAYMENT_STATUS_CHOICES,
    }
    return render(request, 'cms/admin/orders_list.html', context)


@user_passes_test(staff_check, login_url='/cms/login/')
def cms_order_detail(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    if request.method == 'POST':
        form = OrderStatusForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, f"Order {order.order_number} status updated!")
            if request.headers.get('HX-Request'):
                return render(request, 'cms/admin/partials/order_status_badge.html', {'order': order})
            return redirect('cms:order_detail', order_number=order.order_number)
    else:
        form = OrderStatusForm(instance=order)

    return render(request, 'cms/admin/order_detail.html', {'order': order, 'form': form})


@user_passes_test(staff_check, login_url='/cms/login/')
def cms_cake_enquiries(request):
    status_filter = request.GET.get('status')
    enquiries = CustomCakeEnquiry.objects.all()
    if status_filter:
        enquiries = enquiries.filter(status=status_filter)
    enquiries = enquiries.order_by('-created_at')

    context = {
        'enquiries': enquiries,
        'status_filter': status_filter,
        'status_choices': CustomCakeEnquiry.STATUS_CHOICES,
    }
    return render(request, 'cms/admin/cake_enquiries_list.html', context)


@user_passes_test(staff_check, login_url='/cms/login/')
def cms_cake_enquiry_detail(request, reference_number):
    enquiry = get_object_or_404(CustomCakeEnquiry, reference_number=reference_number)
    if request.method == 'POST':
        form = CakeEnquiryStatusForm(request.POST, instance=enquiry)
        if form.is_valid():
            form.save()
            messages.success(request, f"Cake enquiry #{enquiry.reference_number} updated!")
            return redirect('cms:cake_enquiry_detail', reference_number=enquiry.reference_number)
    else:
        form = CakeEnquiryStatusForm(instance=enquiry)

    return render(request, 'cms/admin/cake_enquiry_detail.html', {'enquiry': enquiry, 'form': form})


@user_passes_test(staff_check, login_url='/cms/login/')
def cms_surprise_enquiries(request):
    enquiries = SurprisePackageEnquiry.objects.all().order_by('-created_at')
    return render(request, 'cms/admin/surprise_enquiries_list.html', {'enquiries': enquiries})


@user_passes_test(staff_check, login_url='/cms/login/')
def cms_products(request):
    category_id = request.GET.get('category')
    query = request.GET.get('q', '').strip()

    products = Product.objects.all()
    if category_id:
        products = products.filter(category_id=category_id)
    if query:
        products = products.filter(name__icontains=query)

    products = products.order_by('category', 'display_order', 'name')
    categories = Category.objects.all()

    context = {
        'products': products,
        'categories': categories,
        'selected_category': category_id,
        'query': query,
    }
    return render(request, 'cms/admin/products_list.html', context)


@user_passes_test(staff_check, login_url='/cms/login/')
def cms_product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, f"Product '{product.name}' created successfully!")
            return redirect('cms:products')
    else:
        form = ProductForm()

    return render(request, 'cms/admin/product_form.html', {'form': form, 'title': 'Add New Product'})


@user_passes_test(staff_check, login_url='/cms/login/')
def cms_product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f"Product '{product.name}' updated successfully!")
            return redirect('cms:products')
    else:
        form = ProductForm(instance=product)

    return render(request, 'cms/admin/product_form.html', {'form': form, 'product': product, 'title': f"Edit: {product.name}"})


@user_passes_test(staff_check, login_url='/cms/login/')
@require_POST
def cms_product_toggle_availability(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.is_available = not product.is_available
    product.save(update_fields=['is_available'])
    if request.headers.get('HX-Request'):
        return render(request, 'cms/admin/partials/product_availability_toggle.html', {'product': product})
    return redirect('cms:products')


@user_passes_test(staff_check, login_url='/cms/login/')
def cms_categories(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            cat = form.save()
            messages.success(request, f"Category '{cat.name}' created!")
            return redirect('cms:categories')
    else:
        form = CategoryForm()

    categories = Category.objects.all().annotate(product_count=Count('products')).order_by('display_order', 'name')
    return render(request, 'cms/admin/categories_list.html', {'categories': categories, 'form': form})


@user_passes_test(staff_check, login_url='/cms/login/')
def cms_settings(request):
    site_settings = SiteSettings.get_settings()
    hero = HeroSection.objects.filter(is_active=True).first()

    if request.method == 'POST':
        settings_form = SiteSettingsForm(request.POST, request.FILES, instance=site_settings)
        if settings_form.is_valid():
            settings_form.save()
            messages.success(request, "Site settings and business configuration updated successfully!")
            return redirect('cms:settings')
    else:
        settings_form = SiteSettingsForm(instance=site_settings)

    context = {
        'settings_form': settings_form,
        'site_settings': site_settings,
        'hero': hero,
    }
    return render(request, 'cms/admin/settings.html', context)


# ==========================================
# SEO VIEWS (SITEMAP & ROBOTS.TXT)
# ==========================================

def robots_txt(request):
    host = request.get_host()
    scheme = request.scheme
    content = (
        "User-agent: *\n"
        "Disallow: /admin/\n"
        "Disallow: /cms/\n"
        "Disallow: /checkout/\n"
        "Disallow: /cart/\n"
        "Allow: /\n"
        f"Sitemap: {scheme}://{host}/sitemap.xml\n"
    )
    return HttpResponse(content, content_type="text/plain")


def sitemap_xml(request):
    base_url = f"{request.scheme}://{request.get_host()}"
    urls = [
        {'loc': f"{base_url}/", 'changefreq': 'daily', 'priority': '1.0'},
        {'loc': f"{base_url}/shop/", 'changefreq': 'daily', 'priority': '0.9'},
        {'loc': f"{base_url}/custom-cakes/", 'changefreq': 'weekly', 'priority': '0.9'},
        {'loc': f"{base_url}/surprise-packages/", 'changefreq': 'weekly', 'priority': '0.9'},
        {'loc': f"{base_url}/about/", 'changefreq': 'monthly', 'priority': '0.7'},
        {'loc': f"{base_url}/contact/", 'changefreq': 'monthly', 'priority': '0.7'},
    ]

    for cat in Category.objects.filter(is_active=True):
        urls.append({'loc': f"{base_url}/shop/?category={cat.slug}", 'changefreq': 'daily', 'priority': '0.8'})

    for product in Product.objects.filter(is_available=True):
        urls.append({'loc': f"{base_url}{product.get_absolute_url()}", 'changefreq': 'weekly', 'priority': '0.8'})

    for pkg in SurprisePackage.objects.filter(is_available=True):
        urls.append({'loc': f"{base_url}{pkg.get_absolute_url()}", 'changefreq': 'weekly', 'priority': '0.8'})

    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for u in urls:
        xml_lines.append(f'  <url><loc>{u["loc"]}</loc><changefreq>{u["changefreq"]}</changefreq><priority>{u["priority"]}</priority></url>')
    xml_lines.append('</urlset>')

    return HttpResponse("\n".join(xml_lines), content_type="application/xml")

