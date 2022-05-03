from django.contrib import admin
from .models import Products,Review,Product_Purchase
# Register your models here.
admin.site.register(Products)
admin.site.register(Review)
admin.site.register(Product_Purchase)