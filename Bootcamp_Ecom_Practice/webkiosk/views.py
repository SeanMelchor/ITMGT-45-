from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.forms import ModelForm, HiddenInput
from .models import Product, CartItem, Order
from django.contrib import messages
from .forms import CartItemForm, CheckoutForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json, stripe
from django.conf import settings
from django.db.models import Sum, F

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.
def home(request):
    return render(request, 'webkiosk/home.html')

def products(request):
    products_list = Product.objects.all()

    category_filter = request.GET.get('category')
    sort_by = request.GET.get('sort')

    if category_filter:
        products_list = products_list.filter(category=category_filter)
    
    if sort_by:
        products_list = products_list.order_by(sort_by)

    return render(request, 'webkiosk/products.html', {'products': products_list})

def cart(request): 
    return render(request, 'webkiosk/cart.html')

def aboutus(request): 
    return render(request, 'webkiosk/aboutus.html')

def checkout(request):
    if request.method == 'POST':
        # Extract form data
        full_name = request.POST.get('full_name')
        address = request.POST.get('address')
        email = request.POST.get('email')

        # Extract cart data from hidden input
        cart_data = request.POST.get('cart_data')
        if not cart_data:
            messages.error(request, "Your cart is empty.")
            return redirect('webkiosk:cart')

        try:
            cart = json.loads(cart_data)
        except json.JSONDecodeError:
            messages.error(request, "Invalid cart data.")
            return redirect('webkiosk:cart')

        # Calculate total amount based on cart data
        total_amount = 0
        for item in cart:
            product_id = item.get('id')
            quantity = item.get('quantity', 1)
            try:
                product = Product.objects.get(id=product_id)
                total_amount += product.price * quantity
            except Product.DoesNotExist:
                messages.error(request, f"Product with ID {product_id} does not exist.")
                return redirect('webkiosk:cart')

        if total_amount <= 0:
            messages.error(request, "Total amount must be greater than zero.")
            return redirect('webkiosk:cart')

        # Convert total to cents (Stripe uses the smallest currency unit)
        amount_in_cents = int(total_amount * 100)

        # Create an Order object with status 'Pending'
        order = Order.objects.create(
            items=json.dumps(cart),
            total_price=total_amount,
            full_name=full_name,
            address=address,
            email=email,
            payment_status='Pending',
            shipping_status='Not Shipped'
        )

        # Create Stripe Checkout Session with client_reference_id set to the Order ID
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': amount_in_cents,
                        'product_data': {
                            'name': 'Your Order',
                        },
                    },
                    'quantity': 1,
                }],
                mode='payment',
                client_reference_id=order.id,  # Link the session to the order
                success_url=request.build_absolute_uri(f'/confirmation/?session_id={{CHECKOUT_SESSION_ID}}&order_id={order.id}'),
                cancel_url=request.build_absolute_uri('/checkout/')
            )
        except Exception as e:
            messages.error(request, "There was an error creating your checkout session.")
            # Optionally log the error
            print(f"Stripe Checkout Session creation failed: {e}")
            return redirect('webkiosk:cart')

        # Store the session ID in the order
        order.stripe_session_id = session.id
        order.save()

        return redirect(session.url, code=303)

    else:
        # If GET request, render the checkout page with cart data
        cart = json.loads(request.session.get('cart', '[]'))
        return render(request, 'webkiosk/checkout.html', {
            'stripe_pub_key': settings.STRIPE_PUBLISHABLE_KEY,
            'cart_data': json.dumps(cart)  # Pass cart data to a hidden input
        })

def confirmation(request):
    session_id = request.GET.get('session_id', None)
    order_id = request.GET.get('order_id', None)

    if session_id and order_id:
        try:
            session = stripe.checkout.Session.retrieve(session_id)
        except stripe.error.InvalidRequestError:
            # Invalid session_id
            messages.error(request, "Invalid session.")
            return render(request, 'webkiosk/confirmation.html', {
                'status': 'invalid',
            })

        if session.payment_status == 'paid':
            try:
                order = Order.objects.get(id=order_id, stripe_session_id=session_id)
                order.payment_status = 'Paid'
                order.save()
                # Optionally, clear the cart from session or localStorage
                request.session['cart'] = []  # Clear session cart
                return render(request, 'webkiosk/confirmation.html', {
                    'status': 'success',
                    'order': order
                })
            except Order.DoesNotExist:
                messages.error(request, "Order does not exist.")
                return render(request, 'webkiosk/confirmation.html', {
                    'status': 'invalid',
                })
        else:
            return render(request, 'webkiosk/confirmation.html', {
                'status': 'failed',
                'session': session
            })

    return render(request, 'webkiosk/confirmation.html', {
        'status': 'no_session',
    })

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

@csrf_exempt
def create_order(request):
    print("create_order endpoint hit")  # Debug print
    if request.method == 'POST':
        data = json.loads(request.body)
        print("Data received:", data)  # Debug print

        full_name = data.get('full_name', '')
        address = data.get('address', '')
        email = data.get('email', '')
        cart = data.get('cart', [])
        total = data.get('total', 0)
        

        # Create the order
        order = Order.objects.create(
            items=json.dumps(cart),
            total_price=total,
            full_name=full_name,
            address=address,
            email=email
        )
        
        print("Order created with ID:", order.id)  # Debug print

        return JsonResponse({'status': 'success', 'order_id': order.id})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

def dashboard(request):
    orders = Order.objects.all()
    # Compute total sales
    total_sales = Order.objects.aggregate(total=Sum('total_price'))['total'] or 0

    # Number of orders
    num_orders = Order.objects.count()

    # Average order value
    avg_order_value = total_sales / num_orders if num_orders > 0 else 0

    # Best selling products (top 5 by total revenue)
    best_sellers = (
        CartItem.objects.filter(order__in=orders)
        .values('product__name')
        .annotate(
            total_sold=Sum('quantity'),
            total_revenue=Sum(F('quantity') * F('product__price'))
        )
        .order_by('-total_revenue')[:5]
    )

    context = {
        'total_sales': total_sales,
        'num_orders': num_orders,
        'avg_order_value': avg_order_value,
        'best_sellers': best_sellers,
    }
    return render(request, 'webkiosk/dashboard.html', context)





