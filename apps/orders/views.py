from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime

from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

from .models import Order, OrderItem, Cart, CartItem
from apps.products.models import Product
from apps.accounts.models import Address, Profile

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


def checkout_view(request):
    if request.method == 'POST':
        user = request.user
        cart = get_object_or_404(Cart, customer=user)

        profile, created = Profile.objects.get_or_create(customer=user)

        address = Address.objects.create(
            profile=profile,
            city=request.POST.get('city'),
            district=request.POST.get('district'),
            adress_line_1= request.POST.get('adress_line_1'),
            adress_line_2= request.POST.get('adress_line_2'),
            post_code = request.POST.get('post_code', '')
        )

        try:
            date_delivery = datetime.strptime(request.POST.get('date_delivery'), '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, "Invalid date format. Please use YYYY-MM-DD.")
            return redirect('checkout_view')


        order = Order.objects.create(
            address=address,
            cart=cart,
            date_delivery=date_delivery,
            final_price=cart.total_price,
            final_amount=cart.total_amount
        )

        
        # ✉️ HTML-письмо
        subject = f'Ваш заказ №{order.id} принят'
        from_email = settings.EMAIL_HOST_USER
        to_email = [user.email]

        text_content = f'Спасибо за ваш заказ №{order.id}.'
        html_content = render_to_string('email/order_confirmation_email.html', {
            'user': user,
            'order': order,
        })

        email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
        email.attach_alternative(html_content, "text/html")
        email.send()


        for item in cart.cart_cartitem.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                amount=item.amount,
                total_price=item.total_price
            )

        cart.cart_cartitem.all().delete()
        cart.total_amount = 0
        cart.total_price = 0
        cart.save()
        return redirect('order_success', order_id=order.id)
    return render(request, 'checkout.html', {'cart': cart_context(request).get('cart')})


@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, cart__customer=request.user)
    return render(request, 'order_success.html', {'order': order})








