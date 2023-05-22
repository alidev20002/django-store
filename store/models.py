from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    old_price = models.FloatField()
    price = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    image = models.ImageField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    stock = models.BooleanField(default=True, null=True, blank=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    def serialize(self):
        return {
            'name': self.name,
            'old_price': str(self.old_price),
            'price': str(self.price),
            'category': self.category.name,
            'image': self.image.url,
        }

class Top(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.product.name
    
    def serialize(self):
        return {
            'name': self.product.name,
            'old_price': str(self.product.old_price),
            'price': str(self.product.price),
            'category': self.product.category.name,
            'image': self.product.image.url,
        }

class Spacial(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.product.name

    def serialize(self):
        return {
            'name': self.product.name,
            'old_price': str(self.product.old_price),
            'price': str(self.product.price),
            'category': self.product.category.name,
            'image': self.product.image.url,
        }

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField(default=1, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.user.username + ':' + self.product.name

class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    pay = models.FloatField(default=0)
    name = models.CharField(max_length=200, null=True)
    family = models.CharField(max_length=200, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    postcode = models.CharField(max_length=15, null=True)
    phone = models.CharField(max_length=11, null=True)

    def __str__(self):
        return self.order.user.username + ' ' + str(self.id)