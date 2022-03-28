from django.contrib.auth.models import User
from django.db import models
import datetime
from cloudinary.models import CloudinaryField


class Contact(models.Model):
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    email = models.EmailField(null=False, blank=False)
    message = models.TextField(max_length=2000, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "name: " + self.name, " => subject: " + self.subject


class Customer(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    serial = models.CharField(max_length=50, default='Customer1234')
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=12)
    shipping_address = models.CharField(max_length=200, default='Kitui')
    date = models.DateTimeField(auto_now_add=True)
    image = CloudinaryField('images')
    # image = models.ImageField(upload_to="images", null=False, blank=True, default='Default.jpg')
    idnumber = models.IntegerField(default='1')
    account = models.FloatField(default=0)
    other2 = models.CharField(max_length=50, default='Jane')
    other3 = models.CharField(max_length=50, default='phil')

    def __str__(self):
        return "Serial Number: " + self.serial + " => owner: " + self.name


class Category(models.Model):
    # image = models.ImageField(upload_to="categories", null=False, blank=False, default='Default.jpg')
    image = CloudinaryField('images')
    name = models.CharField(max_length=50, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    cat = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    product_serial = models.CharField(max_length=50)
    name = models.CharField(max_length=50, blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    date_added = models.DateTimeField(auto_now_add=True)
    image = CloudinaryField('images')
    # image = models.ImageField(upload_to="products", null=False, blank=False, default='Default.jpg')
    category = models.CharField(max_length=50, default='General')
    price = models.IntegerField(default=10, blank=False, null=False)
    initprice = models.IntegerField(default=0, blank=False, null=False)
    other3 = models.CharField(max_length=50, default='phil')


class Cart(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product_serial = models.CharField(max_length=15, default='Cart1234', null=False)
    date = models.DateTimeField(auto_now_add=True)
    total_price = models.IntegerField(default=10, blank=False, null=False)
    quantity = models.IntegerField(default=1, null=False)
    image = models.CharField(max_length=500, default='Default.jpg')
    product_name = models.CharField(max_length=50, null=False, default='None')
    customer_name = models.CharField(max_length=100, blank=False, null=False, default='john Doe')
    username = models.CharField(max_length=100, blank=False, null=False, default='john Doe')
    status = models.CharField(max_length=50, default='cart')

    def __str__(self):
        return "Item: " + str(self.product_name)


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default='Transit')
    date = models.DateTimeField(auto_now_add=True)
    price = models.IntegerField(default=10, blank=False, null=False)
    initprice = models.IntegerField(default=0, blank=False, null=False)
    other2 = models.CharField(max_length=50, default='Jane')
