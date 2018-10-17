from django.test import TestCase, Client
from .models import Item, User, Borrow, Review

# #setUp method is called before each test in this class
#    def setUp(self):
#         pass  # nothing to set up

#     def success_response(self):
#         #assumes user with id 1 is stored in db
#         response = self.client.get(reverse('all_orders_list', kwargs={'user_id': 1}))

#         #checks that response contains parameter order list & implicitly
#         # checks that the HTTP status code is 200
#         self.assertContains(response, 'order_list')

#     #user_id not given in url, so error
#     def fails_invalid(self):
#         response = self.client.get(reverse('all_orders_list'))
#         self.assertEquals(response.status_code, 404)

#     #tearDown method is called after each test
#     def tearDown(self):
#         pass  # nothing to tear down


class ItemTestCase(TestCase):
    def setUp(self):
        # User.objects.create(first_name="Brian", last_name="Yu", email="brian@gmail.com", phone_number="1234567890", overview="Hi, my name is Brian!",
        #                     zip_code="12345", lender_rating_total="5", lender_rating_count="20", borrow_rating_total="5", borrow_rating_count="10")
        # User.objects.create(first_name="Brian", last_name="Yu", email="brian@gmail.com", phone_number="1234567890", overview="Hi, my name is Brian!",
        #                     zip_code="12345", lender_rating_total="5", lender_rating_count="20", borrow_rating_total="5", borrow_rating_count="10")
        # Item.objects.create(owner="", title="Paper", condition="", description="",
        #                     price_per_day="", max_borrow_days="", currently_borrowed="")
        # Item.objects.create(owner="", title="Doritos", condition="", description="",
        #                     price_per_day="", max_borrow_days="", currently_borrowed="")
        pass

    def test_getItem(self):
        c = Client()
        response1 = c.get('/api/v1/items/12/')

        response2 = c.get('/api/v1/items/13/')

        self.assertEqual(response1["title"], "10 foot ladder")
        self.assertEqual(response1["owner"], 5)

        self.assertEqual(response2["title"], "car")
        self.assertEqual(response2["owner"], 4)

    # def test_createItem(self):
    #     item1 = Item.objects.get(title="Paper")
    #     item2 = Item.objects.get(title="Doritos")

    #     self.assertEqual(item1.speak(), 'The lion says "roar"')
    #     self.assertEqual(item2.speak(), 'The cat says "meow"')

    # def test_updateItem(self):
    #     item1 = Item.objects.get(title="Paper")
    #     item2 = Item.objects.get(title="Doritos")

    #     self.assertEqual(item1.speak(), 'The lion says "roar"')
    #     self.assertEqual(item2.speak(), 'The cat says "meow"')

    # def test_deleteItem(self):
    #     item1 = Item.objects.get(title="Paper")
    #     item2 = Item.objects.get(title="Doritos")

    #     self.assertEqual(item1.speak(), 'The lion says "roar"')
    #     self.assertEqual(item2.speak(), 'The cat says "meow"')

    # user_id not given in url, so error
    def fails_invalid(self):
        response = self.client.get(reverse('all_orders_list'))
        self.assertEquals(response.status_code, 404)

    # tearDown method is called after each test
    def tearDown(self):
        pass  # nothing to tear down
