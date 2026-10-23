from .models import SiteSettings
from catalog.models import Category, Occasion


def site_settings(request):
    try:
        settings = SiteSettings.get_settings()
    except Exception:
        settings = None

    try:
        nav_categories = Category.objects.filter(is_active=True).order_by('display_order', 'name')
        nav_occasions = Occasion.objects.filter(is_active=True).order_by('display_order', 'name')
    except Exception:
        nav_categories = []
        nav_occasions = []

    return {
        'site_settings': settings,
        'nav_categories': nav_categories,
        'nav_occasions': nav_occasions,
    }
