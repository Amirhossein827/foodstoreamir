from django.contrib import admin
from .models import Category,Food, Order
from django.contrib.auth.models import User

admin.site.register(Category)
admin.site.register(Food)
admin.site.register(Order)
