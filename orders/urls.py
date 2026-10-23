from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/update/<str:key>/', views.cart_update_quantity, name='cart_update'),
    path('cart/remove/<str:key>/', views.cart_remove, name='cart_remove'),
    path('cart/drawer/', views.cart_drawer, name='cart_drawer'),
    path('checkout/', views.checkout, name='checkout'),
    path('confirmation/<str:order_number>/', views.order_confirmation, name='order_confirmation'),
    path('payment/verify/', views.verify_payment, name='verify_payment'),
]
