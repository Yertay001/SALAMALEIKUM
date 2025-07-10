from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Order, OrderItem, Cart, CartItem
from apps.products.models import Product
from apps.accounts.models import Address


@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(customer=request.user, 
                                               defaults={'total_amount': 0, 'total_price': 0})
    
    if created:
        messages.info(request, "Your cart has been created.")
    
    cart_items = CartItem.objects.filter(cart=cart)

    context = {
        'cart': cart,
        'cart_items': cart_items,
    }
    return render(request, 'cart.html', context)

@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart, created = Cart.objects.get_or_create(customer=request.user, 
                                        defaults={'total_amount': 0, 'total_price': 0})
    
    if created:
        messages.info(request, "Your cart has been created.")
    
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'amount': 1})
    
    if not created:      
        cart_item.amount += 1
    else:
        cart.total_amount += 1
    
    cart_item.save()
    cart.total_price += product.price
    cart.save()
    
    messages.success(request, f"{product.title} has been added to your cart.")
    
    return redirect('/')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__customer=request.user)
    cart_item.delete()
    return redirect('cart')
