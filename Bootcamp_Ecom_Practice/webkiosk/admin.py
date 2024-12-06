from django.contrib import admin
from .models import Product, Order

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description', 'image')  
    search_fields = ('name',)  
    list_editable = ('price',)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'address', 'email', 'total_price', 'created_at', 'payment_status', 'shipping_status')
    search_fields = ('full_name', 'email', 'payment_status', 'shipping_status')  

# Optional: If you want to customize the Order admin too:
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ('id', 'total_price', 'created_at', 'payment_status', 'shipping_status')

admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)  # or admin.site.register(Order, OrderAdmin)