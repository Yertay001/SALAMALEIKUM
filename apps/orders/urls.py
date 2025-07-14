from django.urls import path
from .views import add_to_cart, cart_view, increase_amount, decrease_amount, checkout_view,order_success


urlpatterns = [
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart_view, name='cart_view'),
    path('cart/increase/<int:item_id>/', increase_amount, name='increase_amount'),
    path('cart/decrease/<int:item_id>/', decrease_amount, name='decrease_amount'),
    path('checkout/', checkout_view, name='checkout_view'),
    path('order-success/<int:order_id>/', order_success, name='order_success'),
]
