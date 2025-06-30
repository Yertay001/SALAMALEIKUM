from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager

class CustomerManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class Customer(AbstractUser):
    username = None
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name']

    objects = CustomerManager()  # Вот это — обязательно!



    def __str__(self):
        return self.first_name + ' ' + self.last_name
    
class Profile(models.Model):
    GENDER = [
        ('man', 'Man'),
        ('woman', 'Woman'),
    ]
        
    image = models.ImageField(upload_to='profile_images')
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    birth_date = models.DateField()
    gender = models.CharField(max_length=20, choices=GENDER)

    country = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=150, unique=True)

    def _str__(self):
        return f"{self.customer} - {self.gender} - {self.birth_date}"
    
class Address(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    city = models.CharField(max_length=150)
    district = models.CharField(max_length=150)
    adress_line_1 = models.CharField(max_length=150)
    adress_line_2 = models.CharField(max_length=150)
    post_code = models.IntegerField(verbose_name='Индекс')

    def __str__(self):
        return f"{self.city} - {self.district} - {self.adress_line_1} - {self.adress_line_2} - {self.post_code}"  



    




