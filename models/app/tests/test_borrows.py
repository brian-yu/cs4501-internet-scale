from django.test import TestCase
from django.urls import reverse
from app.models import User, Item, Borrow, Review
import json
import urllib.request, urllib.parse
import time

class TestBorrows(TestCase):

    fixtures = ['db.json']
    #setUp method is called before each test in this class
    def setUp(self):
        pass #nothing to set up

    def test_get(self):
        response = self.client.get('http://localhost:8001/api/v1/borrows/3/')
        string = response.content.decode('utf-8')
        response = json.loads(string)['result']

        self.assertEquals(response['lender'], 4)
        self.assertEquals(response['item'], 9)
        self.assertEquals(response['borrower'], 5)
        self.assertEquals(response['borrow_days'], 2)


        response = self.client.get('http://localhost:8001/api/v1/borrows/4/')
        string = response.content.decode('utf-8')
        response = json.loads(string)['result']

        self.assertEquals(response['lender'], 9)
        self.assertEquals(response['item'], 18)   
        self.assertEquals(response['borrower'], 5)
        self.assertEquals(response['borrow_days'], 2)     

        '''
                lender = models.ForeignKey(
                User, on_delete=models.CASCADE, related_name="lent_items")
            borrower = models.ForeignKey(
                User, on_delete=models.CASCADE, related_name="borrowed_items")
            item = models.ForeignKey(Item, on_delete=models.CASCADE)
            borrow_date = models.DateTimeField('date borrowed')
            borrow_days = models.IntegerField(
                validators=[MinValueValidator(1)]
            )
        '''


    def test_create(self):
        post_data = {
            'lender': 8,
            'borrower': 4,
            'item': 17,
            'borrow_date': '2018-10-16 23:43',
            'borrow_days': 365
        }

        post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')

        req = urllib.request.Request('http://localhost:8001/api/v1/borrows/create/', data=post_encoded, method='POST')
        print(req)
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')

        resp = json.loads(resp_json)
        print(resp)

        self.assertEquals(resp['result'], 'ok')

    def test_update(self):
        pass

    def test_delete(self):
        pass


    #tearDown method is called after each test
    def tearDown(self):
        pass #nothing to tear down