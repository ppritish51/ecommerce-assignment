from django.urls import path
from .views import ProductListAPI, ProductDetailAPI

urlpatterns = [
    path('products/', ProductListAPI.as_view(), name='product-list'),
    path('products/<int:id>/', ProductDetailAPI.as_view(), name='product-detail'),
]
