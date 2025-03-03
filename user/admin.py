from django.contrib import admin
from user.models import User, Product, Order, OrderItem
# Register your models here.

class OrderItemInline(admin.TabularInline):
    model = OrderItem

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]

admin.site.register(User)
admin.site.register(Product)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
