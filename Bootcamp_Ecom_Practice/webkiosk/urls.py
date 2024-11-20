from django.http import HttpResponse
from django.urls import path
from . import views


app_name = 'webkiosk'

urlpatterns = [
    path('', views.home, name='home'),
    path('confirmation/', views.confirmation, name='confirmation'),
    path('checkout/', views.checkout, name='checkout'),
    path('product/<int:product_id>/', views.detailProduct, name='product_detail'),
    path('products/', views.products, name='products'),
    path('cart/', views.cart, name='cart'),
    path('aboutus/', views.aboutus, name='aboutus'),
    
]