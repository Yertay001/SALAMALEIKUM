from django.db import models

class UserSegment(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Category(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

class Size(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Product(models.Model):
    COLOR_CHOICES = [
        ('white', 'Белый'),
        ('black', 'Чёрный'),
        ('green', 'Зелёный'),
        ('red', 'Красный'),
        ('blue', 'Синий'),
        ('yellow', 'Жёлтый'),
        ('beige', 'Бежевый'),
        ('gray', 'Серый'),
        ('brown', 'Коричневый'),
        ('pink', 'Розовый'),
        # Добавляй любые другие цвета по мере необходимости
    ]

    
    title = models.CharField(max_length=255)
    user_segment = models.ForeignKey(UserSegment, on_delete=models.CASCADE, related_name='user_segment_product')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_product')
    description = models.TextField(blank=True, null=True)
    article = models.PositiveIntegerField()
    color = models.CharField(max_length=50, choices=COLOR_CHOICES)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, related_name='size_product')
    mane_image = models.ImageField(upload_to='products/main_images/')
    
    TYPE_SALE_CHOICES = [
        ('sale', 'Sale'),
        ('new', 'New'),
        ('best seller', 'Best Seller'),
    ]
    type_sale = models.CharField(max_length=20, choices=TYPE_SALE_CHOICES)

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_productimage')
    image = models.ImageField(upload_to='products/extra_images/')

    def __str__(self):
        return f"Image for {self.product.title}"

