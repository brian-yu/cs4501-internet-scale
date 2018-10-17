from django.test import TestCase, Client
from app.models import Item, User, Borrow, Review
import urllib.request
import urllib.parse
import json

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
    fixtures = ["db.json"]

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
        response1 = json.loads(c.get(
            'http://localhost:8001/api/v1/items/12/').content.decode("utf-8"))
        response2 = json.loads(c.get(
            'http://localhost:8001/api/v1/items/13/').content.decode("utf-8"))

        self.assertEqual(
            response1["result"]["title"], "10 foot ladder")
        self.assertEqual(
            response1["result"]["owner"], 5)

        self.assertEqual(
            response2["result"]["title"], "car")
        self.assertEqual(
            response2["result"]["owner"], 4)

    def test_createItem(self):
        post_data1 = {'owner': 5,
                      'title': "My Dog", 'condition': "E", "description": "Dogs.", "price_per_day": "50.00", "max_borrow_days": 10, "currently_borrowed": True}
        post_data2 = {'owner': 4,
                      'title': "My Cat", 'condition': "G", "description": "Cats.", "price_per_day": "25.00", "max_borrow_days": 5, "currently_borrowed": False}

        post_encoded1 = urllib.parse.urlencode(post_data1).encode('utf-8')
        post_encoded2 = urllib.parse.urlencode(post_data2).encode('utf-8')

        req1 = urllib.request.Request(
            'http://localhost:8001/api/v1/items/create/', data=post_encoded1, method='POST')
        req2 = urllib.request.Request(
            'http://localhost:8001/api/v1/items/create/', data=post_encoded2, method='POST')

        print(req1)
        print(req2)

        resp_json1 = json.loads(
            urllib.request.urlopen(req1).decode('utf-8'))
        resp_json2 = json.loads(
            urllib.request.urlopen(req2).decode('utf-8'))

        print(resp_json1)
        print(resp_json2)

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
        # def fails_invalid(self):
        #     response = self.client.get(reverse('all_orders_list'))
        #     self.assertEquals(response.status_code, 404)

        # # tearDown method is called after each test
        # def tearDown(self):
        #     pass  # nothing to tear down
