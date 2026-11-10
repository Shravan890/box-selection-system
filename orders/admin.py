from django.contrib import admin
from .models import Box, Order, OrderItem, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("sku", "name", "length", "width", "height", "weight")
    search_fields = ("sku", "name")


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_display = ("name", "length", "width", "height", "max_weight", "cost")


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "recommended_box")
    inlines = (OrderItemInline,)
    readonly_fields = ("created_at", "recommendation_note")
