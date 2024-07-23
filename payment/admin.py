from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem


# Register your models here.
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)

#Create an order item inline
class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    model = Order
    fields = ['date_ordered', 'user', 'full_name','email', 'Shipping_address', 'amount_paid', 'shipped', 'date_shipped']
    inlines = [OrderItemInline]
    readonly_fields = ['date_ordered']

#Unregister the Order Model
admin.site.unregister(Order)

#Re-register the Order Model
admin.site.register(Order, OrderAdmin)
