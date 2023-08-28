from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    rating = models.FloatField()
    price = models.FloatField()
    image = models.CharField(max_length=10000)
    # image = models.ImageField(upload_to='uploads')

    def __str__(self):
        return self.name
    


class Wishlist(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name
    

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    product_quantity=models.IntegerField(default=1)

    def __str__(self):
        return self.product.name
    
class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    Product = models.ForeignKey(Product,on_delete=models.CASCADE,default=0)
    product_quantity=models.IntegerField(default=0)
    total_rupess=models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    message = models.TextField()

    def __str__(self):
        return self.name