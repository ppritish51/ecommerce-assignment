# cart/urls.py

from django.urls import path
from .views import AddToCartAPI, RemoveFromCartAPI, GetCartAPI

urlpatterns = [
    path('add/', AddToCartAPI.as_view(), name='add-to-cart'),
    path('remove/', RemoveFromCartAPI.as_view(), name='remove-from-cart'),
    path('', GetCartAPI.as_view(), name='get-cart'),
]

