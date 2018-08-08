from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['book']
    readonly_fields = "book", "order", "price", "quantity"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'paid', 'created', 'updated']
    search_fields = 'first_name', 'last_name', 'email'
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    readonly_fields = ['id', 'first_name', 'last_name', 'email',
                       'created', 'updated', 'tx_ref']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    '''Admin View for OrderItem'''

    list_display = "book", "order", "price", "quantity"
    list_filter = ('book',)

    readonly_fields = "book", "order", "price", "quantity"
