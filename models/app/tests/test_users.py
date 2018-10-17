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


class TestUsers(TestCase):
    fixtures = ["db.json"]

    def setUp(self):
        pass

    def test_get_user(self):
        c = Client()
        recv_json = c.get(
            'http://localhost:8000/api/v1/users/4/'
            ).content.decode("utf-8")
        recv_dict = json.loads(recv_json)
        expected_json = r"""{"ok": true, "result": {"last_name": "Yu", "borrower_rating_total": 0, "lender_rating_total": 0, "borrower_rating_count": 0, "email": "bry4xm@virginia.edu", "id": 4, "zip_code": "22903", "overview": "heh", "lender_rating_count": 0, "phone_number": "", "first_name": "Brian"}}"""
        exp_dict = json.loads(expected_json)
        self.assertEqual(
            recv_dict, exp_dict)
        

    # def test_create_user(self):
    #     post_data1 = {'owner': 5,
    #                   'title': "My Dog", 'condition': "E", "description": "Dogs.", "price_per_day": "50.00", "max_borrow_days": 10, "currently_borrowed": True}
    #     post_data2 = {'owner': 4,
    #                   'title': "My Cat", 'condition': "G", "description": "Cats.", "price_per_day": "25.00", "max_borrow_days": 5, "currently_borrowed": False}

    #     response1 = self.client.post('http://models-api:8001/api/v1/items/create/', post_data1, format='json')
    #     response2 = self.client.post('http://models-api:8001/api/v1/borrows/create/', post_data2, format='json')
