from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description', 'image')  # Display columns in the admin list view
    search_fields = ('title',)  # Add search functionality by title

    # Make the image field editable in the list view (optional)
    list_editable = ('price',)  # Only price can be edited directly in the list view, for example

admin.site.register(Product, ProductAdmin)

# Register your models here.
