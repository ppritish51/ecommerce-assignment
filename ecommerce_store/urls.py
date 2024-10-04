
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin panel access
    path('cart/', include('cart.urls')),  # Cart app URLs
    path('orders/', include('orders.urls')),  # Orders app URLs
    path('products/', include('products.urls')),  # Discounts app URLs

    # Optional: DRF's browsable API login
    path('api-auth/', include('rest_framework.urls')),
]

