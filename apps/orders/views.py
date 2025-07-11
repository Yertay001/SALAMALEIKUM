from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Order, OrderItem, Cart, CartItem
from apps.products.models import Product
from apps.accounts.models import Address

def cart_context(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(customer=request.user).order_by('-id').first()
        return {'cart': cart}
    return {'cart': None}

@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(customer=request.user,
                                               defaults={'total_amount': 0, 'total_price': 0})
    
    if created:
        messages.info(request, "Your cart has been created.")

    cart_items = CartItem.objects.filter(cart=cart).select_related('product').prefetch_related('product__favorite_set')


    context = {
        'cart': cart,
        'cart_items': cart_items,
    }
    return render(request, 'cart.html', context)
    

login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart, created = Cart.objects.get_or_create(customer=request.user,
                                               defaults={'total_amount': 0, 'total_price': 0})
    
    if created:
        messages.info(request, "Your cart has been created.")

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'amount': 1})

    if not created:
        cart_item.amount += 1

    cart.total_amount += 1

    cart_item.save()
    cart.total_price += product.price
    cart.save()

    messages.success(request, f"{product.title} has been added to your cart.")

    return redirect('cart_view')

login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__customer=request.user)
    cart_item.delete()
    return redirect('cart')


@login_required
def increase_amount(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__customer=request.user)
    cart_item.amount += 1
    cart_item.save()

    cart = cart_item.cart
    cart.total_amount += 1
    cart.total_price += cart_item.product.price
    cart.save()

    return redirect('cart_view')


@login_required
def decrease_amount(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__customer=request.user)
    cart = cart_item.cart

    if cart_item.amount > 1:
        cart_item.amount -= 1
        cart_item.save()
        cart.total_amount -= 1
        cart.total_price -= cart_item.product.price
    else:
        cart.total_amount -= 1
        cart.total_price -= cart_item.product.price
        cart_item.delete()

    # 🛡 Защита от отрицательных значений
    if cart.total_amount < 0:
        cart.total_amount = 0
    if cart.total_price < 0:
        cart.total_price = 0

    cart.save()
    return redirect('cart_view')










