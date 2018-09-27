from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User as DjangoUser
from django.contrib.localflavor.us.models import USZipCodeField

class User(models.Model):
    user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE)
    zip_code = USZipCodeField()

class Item(models.Model):
    EXCELLENT = 'E'
    GOOD = 'G'
    OKAY = 'O'
    BAD = 'B'
    CONDITION_CHOICES = (
        (EXCELLENT, 'E'),
        (GOOD, 'G'),
        (OKAY, 'O'),
        (BAD, 'B'),
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    condition = models.CharField(
        max_length=1,
        choices=CONDITION_CHOICES,
        default=GOOD,)
    description = models.TextField()
    price_per_day = models.DecimalField(decimal_places=2)
    max_borrow_days = models.IntegerField(
        validators = [MinValueValidator(1)]
    )


class Borrow(models.Model):
    lender = models.ForeignKey(User, on_delete=models.CASCADE)
    borrower = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField('date borrowed')
    borrow_days = models.DurationField()