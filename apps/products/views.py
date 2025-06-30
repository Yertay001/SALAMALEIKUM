from django.shortcuts import render
from apps.products.models import UserSegment, Category, Size, Product, ProductImage

def index(request):
    context = {
        'UserSegment': UserSegment.objects.all(),
        'Category': Category.objects.all(),
        'Size': Size.objects.all(),
        'Product': Product.objects.all(),
        'ProductImage': ProductImage.objects.all(),
    }
    return render(request, 'index.html', context=context)
