from django.test import TestCase
from .models import Item, User, Borrow, Review


class ItemTestCase(TestCase):
    def setUp(self):
        User.objects.create(first_name="Brian", last_name="Yu", email="brian@gmail.com", phone_number="1234567890", overview="Hi, my name is Brian!",
                            zip_code="12345", lender_rating_total="5", lender_rating_count="20", borrow_rating_total="5", borrow_rating_count="10")
        User.objects.create(first_name="Brian", last_name="Yu", email="brian@gmail.com", phone_number="1234567890", overview="Hi, my name is Brian!",
                            zip_code="12345", lender_rating_total="5", lender_rating_count="20", borrow_rating_total="5", borrow_rating_count="10")
        Item.objects.create(owner="", title="Paper", condition="", description="",
                            price_per_day="", max_borrow_days="", currently_borrowed="")
        Item.objects.create(owner="", title="Doritos", condition="", description="",
                            price_per_day="", max_borrow_days="", currently_borrowed="")

    def test_item(self):
        item1 = Item.objects.get(title="Paper")
        item2 = Item.objects.get(title="Doritos")

        self.assertEqual(item1.speak(), 'The lion says "roar"')
        self.assertEqual(item2.speak(), 'The cat says "meow"')
