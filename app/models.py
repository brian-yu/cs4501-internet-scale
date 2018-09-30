from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    overview = models.TextField() # an optional introduction about the user's expertise/hobbies
    zip_code = models.CharField(
        max_length = 10,
        validators=[RegexValidator(r'^\d{5}(?:[-\s]\d{4})?$')]
    )
    lender_rating_total = models.IntegerField()
    lender_rating_count = models.IntegerField()
    borrower_rating_total = models.IntegerField()
    borrower_rating_count = models.IntegerField()

    def __str__(self):
        return self.first_name + " " + self.last_name

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

    def __str__(self):
        return self.title + " owned by " + self.owner.__str__()

class Borrow(models.Model):
    lender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lent_items")
    borrower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="borrowed_items")
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField('date borrowed')
    borrow_days = models.IntegerField(
        validators = [MinValueValidator(1)]
    )
    def __str__(self):
        return self.borrower.__str__() + " borrowing " + self.item.__str__()

class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="written_reviews")
    reviewee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_reviews")
    text = models.TextField()
    score = models.IntegerField(
        validators = [MinValueValidator(1), MaxValueValidator(5)]
    )
    def __str__(self):
        return self.reviewer.__str__() + "'s review of " + self.reviewee.__str__()