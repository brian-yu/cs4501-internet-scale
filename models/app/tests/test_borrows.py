from django.test import TestCase
from django.urls import reverse
from app.models import User, Item, Borrow, Review
import json
import urllib.request, urllib.parse
import time
from django.db import transaction

class TestBorrows(TestCase):

    fixtures = ['db.json']
    
    #setUp method is called before each test in this class
    def setUp(self):
        pass

    def test_get_success(self):
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

    def test_get_fail(self):
        res = json.loads(self.client.get(
            'http://localhost:8001/api/v1/borrows/100/'
            ).content.decode("utf-8"))
        expected = json.loads(
            r"""{"error": "Borrow with id=100 not found", "ok": false}"""
            )
        self.assertEqual(res, expected)


    def test_create_success(self):
        post_data = {
            'lender': 8,
            'borrower': 4,
            'item': 17,
            'borrow_date': '2018-10-16 23:43',
            'borrow_days': 365
        }

        response = self.client.post('http://models-api:8001/api/v1/borrows/create/', post_data, format='json')
        self.assertEquals(response.status_code, 200)

        string = response.content.decode('utf-8')
        response = json.loads(string)
        self.assertEquals(response['ok'], True)

    def test_create_fail(self):
        form_data = {
            'lender': 8,
            'borrower': 4,
            'item': 17,
            'borrow_date': 1000, # invalid date format
            'borrow_days': 1
        }

        res = json.loads(self.client.post('http://localhost:8001/api/v1/borrows/create/', form_data, format='json').content.decode('utf-8'))

        self.assertEqual("error" in res, True)
        self.assertEqual(res["ok"], False)

        form_data = {
            'lender': 8,
            'borrower': 4,
            'item': 17,
            'borrow_date': '2018-10-16 23:43',
            'borrow_days': 0 # invalid borrow days
        }

        res = json.loads(self.client.post('http://localhost:8001/api/v1/borrows/create/', form_data, format='json').content.decode('utf-8'))

        self.assertEqual("error" in res, True)
        self.assertEqual(res["ok"], False)

        form_data = { # not enough data
            'lender': 8,
            'borrower': 4,
        }

        res = json.loads(self.client.post('http://localhost:8001/api/v1/borrows/create/', form_data, format='json').content.decode('utf-8'))

        self.assertEqual("error" in res, True)
        self.assertEqual(res["ok"], False)


    def test_update(self):
        post_data = {'borrow_days': 10}
        response = self.client.post('http://models-api:8001/api/v1/borrows/5/', post_data, format='json')
        self.assertEquals(response.status_code, 200)

        string = response.content.decode('utf-8')
        response = json.loads(string)
        self.assertEquals(response['ok'], True)

        self.assertEquals(Borrow.objects.get(id=5).borrow_days, 10)


    def test_update_fails(self):
        form_data = {'borrow_date': '2018/10/5'} # invalid date format
        res = json.loads(self.client.post('http://localhost:8000/api/v1/borrows/10/', form_data, format='json').content.decode('utf-8'))
        
        exp = json.loads(r"""{"error": "Borrow with id=10 not found", "ok": false}""")
        self.assertEqual(res, exp)


    def test_delete(self):

        borrow = Borrow.objects.create(
                    lender=User.objects.get(id=8),
                    item=Item.objects.get(id=16),
                    borrower=User.objects.get(id=5),
                    borrow_date='2018-10-17 23:43',
                    borrow_days=3
                )

        num_borrows = Borrow.objects.count()
        response = self.client.delete('http://models-api:8001/api/v1/borrows/{}/delete/'.format(borrow.id))
        self.assertEquals(response.status_code, 200)

        self.assertEquals(num_borrows, Borrow.objects.count() + 1)

        string = response.content.decode('utf-8')
        response = json.loads(string)
        self.assertEquals(response['ok'], True)


    def test_delete_fails(self):
        res = json.loads(self.client.delete('http://localhost:8000/api/v1/borrows/100/delete/').content.decode('utf-8'))
        
        exp = json.loads(r"""{"error": "Borrow with id=100 not found", "ok": false}""")
        self.assertEqual(res, exp)


    #tearDown method is called after each test
    def tearDown(self):
        pass