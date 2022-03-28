from django.contrib import admin
from .models import Contact, Customer, Cart, Product, Order, Category

# Register your models here.
admin.site.register(Contact)
admin.site.register(Customer)
admin.site.register(Cart)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Category)
