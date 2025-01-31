from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Contact(models.Model):
    name= models.CharField(max_length= 200,null=True)
    email= models.EmailField()
    sub= models.CharField(max_length=200,null=True)
    message= models.CharField(max_length= 200,null=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    image=models.ImageField(upload_to='product/',blank=True, null=True)
    name = models.CharField(max_length=100,null=False,blank=False)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE,default=False,null=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Cart {self.id} - {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='products', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Cart {self.cart.user.username}"

