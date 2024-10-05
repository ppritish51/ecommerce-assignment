from django.contrib import admin
from .models import Order, OrderItem, DiscountCode


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_price', 'discount_value', 'created_at']
    inlines = [OrderItemInline]
    list_filter = ['created_at']
    search_fields = ['user__username']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price']
    search_fields = ['order__user__username', 'product__name']


@admin.register(DiscountCode)
class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_percentage', 'is_used', 'created_at']
    list_filter = ['is_used', 'created_at']
    search_fields = ['code']
