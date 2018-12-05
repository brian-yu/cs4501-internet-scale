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
        self.client = Client()

    def test_getItem_Success(self):
        response1 = json.loads(self.client.get(
            'http://localhost:8001/api/v1/items/12/').content.decode("utf-8"))

        self.assertEqual(
            response1["result"]["owner"], "Aaron Gu")

    def test_getItem_Fail(self):
        response1 = json.loads(self.client.get(
            'http://localhost:8001/api/v1/items/1000/').content.decode("utf-8"))
        test = json.loads(
            r"""{"error": "Item with id=1000 not found", "ok": false}""")

        self.assertEqual(response1, test)

    def test_createItem_Success(self):
        post_data1 = {'owner': 10,
                      'title': "My Dog", 'condition': "E", "description": "Dogs.", "price_per_day": "50.00", "max_borrow_days": 15, 'currently_borrowed': True}
        response1 = json.loads(self.client.post(
            'http://models-api:8001/api/v1/items/create/', post_data1, format='json').content.decode('utf-8'))

        self.assertEqual(
            response1["result"]["max_borrow_days"], 15)
        self.assertEqual(
            response1["result"]["title"], 'My Dog')
        self.assertEqual(
            response1["result"]["condition"], 'E')
        self.assertEqual(
            response1["result"]["description"], 'Dogs.')
        self.assertEqual(
            response1["result"]["price_per_day"], '50.00')
        self.assertEqual(response1["result"]["currently_borrowed"], 'True')
        self.assertEqual(
            response1["result"]["owner"], 10)

    def test_createItem_Fail(self):
        post_data = {
            'title': 'helllo',
            'condition': 'E'
        }
        test = json.loads(self.client.post('http://localhost:8000/api/v1/items/create/',
                                           post_data, format='json').content.decode('utf-8'))
        self.assertEqual("error" in test, True)
        self.assertEqual(test["ok"], False)

    def test_updateItem_Success(self):
        title = {'title': 'Updated The Dog'}
        update = json.loads(self.client.post(
            "http://localhost:8001/api/v1/items/12/", title, format="json").content.decode("utf-8"))
        get = json.loads(self.client.get(
            'http://localhost:8000/api/v1/items/12/').content.decode('utf-8'))


        self.assertEqual('ok' in get, True)
        self.assertEqual('ok' in update, True)

    def test_updateItem_Fail(self):
        title = {'title': 'Updated The Dog'}
        update = json.loads(self.client.post(
            "http://localhost:8000/api/v1/items/1000/", title, format="json").content.decode("utf-8"))

        exp = json.loads(
            r"""{"error": "Item with id=1000 not found", "ok": false}""")
        self.assertEqual(update, exp)

    def test_deleteItem_Success(self):
        delete = json.loads(self.client.delete(
            'http://localhost:8000/api/v1/items/13/delete/', "", format='json').content.decode('utf-8'))

        whatitshouldbe = json.loads(r"""{"ok": true}""")
        self.assertEqual(delete, whatitshouldbe)

        toget = json.loads(self.client.get(
            'http://localhost:8000/api/v1/items/4/').content.decode('utf-8'))
        whatitshouldbe = json.loads(
            r"""{"error": "Item with id=4 not found", "ok": false}""")
        self.assertEqual(toget, whatitshouldbe)

    def test_deleteItem_Fail(self):
        delete = json.loads(self.client.delete(
            'http://localhost:8000/api/v1/items/1000/delete/', "", format='json').content.decode('utf-8'))

        whatitshouldbe = json.loads(
            r"""{"error": "Item with id=1000 not found", "ok": false}""")
        self.assertEqual(delete, whatitshouldbe)