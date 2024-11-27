from django.db import models
import datetime

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)

class Food(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='foods/')
    is_sale = models.BooleanField(default=False)
    sale_price = models.IntegerField(default=0)
    existing = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Order(models.Model):
	product = models.ForeignKey(Food, on_delete=models.CASCADE)
	# customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
	quantity = models.IntegerField(default=1)
	address = models.CharField(max_length=100, default='', blank=True)
	phone = models.CharField(max_length=20, default='', blank=True)
	date = models.DateField(default=datetime.datetime.today)
	status = models.BooleanField(default=False)

	def __str__(self):
		return self.product