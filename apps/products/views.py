from django.shortcuts import render
from .models import Product, Category, UserSegment

def index(request):
    # Получение параметров из URL
    category = request.GET.get('category')
    usersegment = request.GET.get('usersegment')
    type_sale = request.GET.get('type')
    color = request.GET.get('color')
    size = request.GET.get('size')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    products = Product.objects.all()

    if category:
        products = products.filter(category__title=category)

    if usersegment:
        products = products.filter(user_segment__name=usersegment)

    if type_sale:
        products = products.filter(type_sale=type_sale)

    if color:
        products = products.filter(color=color)

    if size:
        products = products.filter(size__name=size)

    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)

    categories = Category.objects.all()
    usersegments = UserSegment.objects.all()

    context = {
        'products': products,
        'categories': categories,
        'usersegments': usersegments,
        'active_filters': {
            'category': category,
            'usersegment': usersegment,
            'type': type_sale,
            'color': color,
            'size': size,
            'min_price': min_price,
            'max_price': max_price,
        },
        'type_choices': ['new', 'bestseller', 'sale'],
        'color_choices': ['black', 'white', 'gray', 'red', 'blue', 'green', 'orange', 'purple'],
        'size_choices': ['s', 'm', 'l', 'xl']
    }
    return render(request, 'index.html', context)



