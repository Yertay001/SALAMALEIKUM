from django.db import models
from apps.accounts.models import Address, Customer
from apps.products.models import Product 


class Cart(models.Model):
    customer= models.ForeignKey(Customer, on_delete=models.CASCADE,related_name="customer_cart")
    total_amount= models.IntegerField()
    total_price= models.DecimalField(max_digits=20, decimal_places=2)
    
    def __str__(self):
        return f"{self.customer.first_name} - {self.total_amount} - {self.total_price}"

class CartItem(models.Model):
    cart=models.ForeignKey(Cart, on_delete=models.CASCADE,related_name="cart_cartitem")
    amount= models.PositiveIntegerField()
    product= models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_cartitem")

    def __str__(self):
        return f"{self.cart.customer.first_name} - {self.amount} - {self.product}"

# Create your models here.
class Order(models.Model):
    address = models.ForeignKey(Address, on_delete=models.CASCADE,related_name="address_order")
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE, related_name= "cart_order" )
    created_at=models.DateTimeField(auto_now_add=True)
    date_delivery=models.DateField()
    final_price = models.DecimalField(max_digits=20, decimal_places=2)
    final_amount = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.address} - {self.date_delivery} - {self.final_price}"
    
class OrderItem(models.Model):
    order=models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_orderitem")
    product=models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_oredreitem")
    amount= models.PositiveIntegerField()
    total_price=models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return f"{self.product.title} - {self.amount} - {self.total_price}"

    