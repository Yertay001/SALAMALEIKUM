from django.contrib import admin
from .models import Product, Category, Size, UserSegment, ProductImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'type_sale', 'article')
    search_fields = ('title', 'description', 'color')
    list_filter = ('category', 'type_sale', 'color', 'user_segment')
    autocomplete_fields = ('category', 'size', 'user_segment')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ('title',)


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(UserSegment)
class UserSegmentAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image')

    
