from django.db import models
from django.contrib.auth.models import AbstractUser

class Customer(AbstractUser):
    username = models.CharField(max_length=150, blank=True, null=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=150, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name']

    def __str__(self):
        return self.first_name + ' ' + self.last_name
    
class Profile(models.Model):
    GENDER = [
        ('man', 'Man'),
        ('woman', 'Woman'),
    ]
        
    image = models.ImageField(upload_to='profile_images')
    customer = models.OneToOneField(Customer, on_delete=Customer)
    birth_date = models.DateField()
    gender = models.CharField(max_length=20, choices=GENDER)

    country = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=150, unique=True)

    def _str__(self):
        return f"{self.customer} - {self.gender} - {self.birth_date}"
    
class Address(models.Model):
    profile = models.ForeignKey(Profile, on_delete=Profile)
    city = models.CharField(max_length=150)
    district = models.CharField(max_length=150)
    adress_line_1 = models.CharField(max_length=150)
    adress_line_2 = models.CharField(max_length=150)
    post_code = models.IntegerField(verbose_name='Индекс')

    def __str__(self):
        return f"{self.city} - {self.district} - {self.adress_line_1} - {self.adress_line_2} - {self.post_code}"  



    




