from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    category = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name
    
class Order(models.Model):
    items = models.TextField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    payment_status = models.CharField(max_length=50, default='Pending')  # e.g. 'Pending', 'Paid', 'Shipped'
    shipping_status = models.CharField(max_length=50, default='Not Shipped')  # e.g. 'Not Shipped', 'Shipped', 'Delivered'

    def __str__(self):
        return f"Order {self.id}"
    
class CartItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def totalprice(self):
        return self.quantity * self.product.price

