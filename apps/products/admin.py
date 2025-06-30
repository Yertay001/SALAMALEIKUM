from django.contrib import admin
from apps.products.models import UserSegment, Category, Size, Product, ProductImage

admin.site.register(UserSegment)
admin.site.register(Category)
admin.site.register(Size)
admin.site.register(Product)
admin.site.register(ProductImage)

