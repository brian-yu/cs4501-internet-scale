from django.db import models
from django.core.validators import MinValueValidator, RegexValidator
from django.contrib.auth.models import User as DjangoUser

class User(models.Model):
    user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE)
    zip_code = models.CharField(
        max_length = 10,
        validators=[RegexValidator(r'^\d{5}(?:[-\s]\d{4})?$')]
    )

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
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    max_borrow_days = models.IntegerField(
        validators = [MinValueValidator(1)]
    )
    currently_borrowed = models.BooleanField()


class Borrow(models.Model):
    lender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lent_items")
    borrower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="borrowed_items")
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField('date borrowed')
    borrow_days = models.IntegerField(
        validators = [MinValueValidator(1)]
    )