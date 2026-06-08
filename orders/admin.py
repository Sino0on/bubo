from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'product', 'color', 'quantity', 'delivery_method', 'status', 'created_at')
    list_filter = ('status', 'delivery_method', 'created_at')
    search_fields = ('name', 'phone', 'product__name')
    list_editable = ('status',)
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
