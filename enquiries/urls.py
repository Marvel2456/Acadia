from django.urls import path
from . import views

app_name = 'enquiries'

urlpatterns = [
    path('custom-cakes/', views.custom_cake_request, name='custom_cake'),
    path('custom-cakes/confirmation/<str:reference_number>/', views.custom_cake_confirmation, name='cake_confirmation'),
    path('surprise-packages/', views.surprise_package_list, name='surprise_packages'),
    path('surprise-packages/<slug:slug>/', views.surprise_package_detail, name='package_detail'),
    path('surprise-packages/confirmation/<str:reference_number>/', views.surprise_package_confirmation, name='package_confirmation'),
]
