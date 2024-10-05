
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin panel access
    path('cart-api/', include('cart.urls')),  # Cart app URLs
    path('orders-api/', include('orders.urls')),  # Orders app URLs
    path('products-api/', include('products.urls')),  # Discounts app URLs

    # Optional: DRF's browsable API login
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]

