from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import *

app_name = 'cart'

urlpatterns = [
    path('my_cart', login_required(CartView.as_view(), login_url='home:login'), name='my_cart'),
    path('delete_item/<str:slug>', delete_cart, name='delete_item'),
    path('increase_quantity/<str:slug>', increase_quantity, name='increase_quantity'),
    path('decrease_quantity/<str:slug>', decrease_quantity, name='decrease_quantity'),
    path('add_to_wishlist/<str:slug>', add_to_wishlist, name='add_to_wishlist'),
    path('my_wishlist/', login_required(WishlistView.as_view(), login_url='home:login'), name='my_wishlist'),
    path('delete_wishlist/<str:slug>', delete_wishlist, name='delete_wishlist'),
    path('contact/', contact, name='contact'),
    path('add-to-cart/', addToCart, name='addToCart'),
]