from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from apps.products.models import Product
from .models import Favorite

@login_required
def toggle_favorite(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)

    if not created:
        favorite.delete()  # если уже был — удалим
    return redirect(request.META.get('HTTP_REFERER', 'products:product_list'))  # вернуться на ту же страницу

@login_required
def favorites_list(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('product')
    return render(request, 'favorites_list.html', {'favorites': favorites})
