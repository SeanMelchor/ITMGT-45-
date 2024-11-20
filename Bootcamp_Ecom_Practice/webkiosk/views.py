from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.forms import ModelForm, HiddenInput
from .models import Product, CartItem, Order
from django.contrib import messages
from .forms import CartItemForm, CheckoutForm

# Create your views here.
def home(request):
    return render(request, 'webkiosk/home.html')

def products(request): 
    products_list = Product.objects.all()
    return render(request, 'webkiosk/products.html', {'products': products_list})

def cart(request): 
    return render(request, 'webkiosk/cart.html')

def aboutus(request): 
    return render(request, 'webkiosk/aboutus.html')

def checkout(request):
    return render(request, 'webkiosk/checkout.html')

def confirmation(request):
    return render(request, 'webkiosk/confirmation.html')

def detailProduct(request, product_id):
    # Adds a product to the cart
    product = get_object_or_404(Product, id=product_id)
    # Handle adding the product to the cart
    if request.method == 'POST':
        form = CartItemForm(request.POST)
        if form.is_valid():
            # Get or create an order
            order, created = Order.objects.get_or_create(id=request.session.get('order_id'))
            # Create or update the cart item for the current product
            cart_item, created = CartItem.objects.get_or_create(
                product=product, order=order)
            # Update the quantity of the cart item
            cart_item.quantity += form.cleaned_data['quantity']
            cart_item.save()
            return redirect('view_cart')
    else:
        form = CartItemForm()
    return render(request, 'products.html', {'product': product, 'form': form})





