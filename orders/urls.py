# orders/urls.py

from django.urls import path
from .views import CheckoutAPI, OrderHistoryAPI, ValidateDiscountAPI

urlpatterns = [
    path('checkout/', CheckoutAPI.as_view(), name='checkout'),
    path('order-history/', OrderHistoryAPI.as_view(), name='order-history'),
    path('validate-discount/', ValidateDiscountAPI.as_view(), name='validate-discount'),
]
