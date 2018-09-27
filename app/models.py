from django.db import models
from django.contrib.auth.models import User as DjangoUser

class User(models.Model):
    user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE)

class Item(models.Model):
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	condition = models.CharField(max_length=20)
	description = models.TextField()
	price_per_day = models.DecimalField(decimal_places=2)

class Borrow(models.Model):
	lender = models.ForeignKey(User, on_delete=models.CASCADE)
	borrower = models.ForeignKey(User, on_delete=models.CASCADE)
	item = models.ForeignKey(Item, on_delete=models.CASCADE)
	borrow_date = models.DateTimeField('date borrowed')
	borrow_duration = models.DurationField()