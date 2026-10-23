from django.urls import path
from . import views

app_name = 'cms'

urlpatterns = [
    # Public views
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),

    # Staff CMS views
    path('cms/login/', views.cms_login_view, name='login'),
    path('cms/logout/', views.cms_logout_view, name='logout'),
    path('cms/', views.cms_dashboard, name='dashboard'),
    path('cms/orders/', views.cms_orders, name='orders'),
    path('cms/orders/<str:order_number>/', views.cms_order_detail, name='order_detail'),
    path('cms/cake-enquiries/', views.cms_cake_enquiries, name='cake_enquiries'),
    path('cms/cake-enquiries/<str:reference_number>/', views.cms_cake_enquiry_detail, name='cake_enquiry_detail'),
    path('cms/surprise-enquiries/', views.cms_surprise_enquiries, name='surprise_enquiries'),
    path('cms/products/', views.cms_products, name='products'),
    path('cms/products/create/', views.cms_product_create, name='product_create'),
    path('cms/products/<int:pk>/edit/', views.cms_product_edit, name='product_edit'),
    path('cms/products/<int:pk>/toggle/', views.cms_product_toggle_availability, name='product_toggle'),
    path('cms/categories/', views.cms_categories, name='categories'),
    path('cms/settings/', views.cms_settings, name='settings'),
]
