from django.test import TestCase
from django.urls import reverse
from app.models import User, Item, Borrow, Review
import json

class TestReviews(TestCase):

    fixtures = ['db.json']
    
    #setUp method is called before each test in this class
    def setUp(self):
        pass

    def test_get_success(self):
        response = self.client.get('http://localhost:8001/api/v1/reviews/3/')
        string = response.content.decode('utf-8')
        response = json.loads(string)['result']

        self.assertEquals(response['reviewer'], 5)
        self.assertEquals(response['reviewee'], 4)

    def test_get_fail(self):
        res = json.loads(self.client.get(
            'http://localhost:8001/api/v1/reviews/100/'
            ).content.decode("utf-8"))
        expected = json.loads(
            r"""{"error": "Review with id=100 not found", "ok": false}"""
            )
        self.assertEqual(res, expected)


    def test_create_success(self):
        post_data = {
            'reviewer': 8,
            'reviewee': 5,
            'text': 'excellent condition product',
            'score': 5
        }

        response = self.client.post('http://models-api:8001/api/v1/reviews/create/', post_data, format='json')
        self.assertEquals(response.status_code, 200)

        string = response.content.decode('utf-8')
        response = json.loads(string)
        self.assertEquals(response['ok'], True)

    def test_create_fail(self):
        form_data = {
        	'reviewer': 'fizzbuzz', # invalid foreign key to user
        	'reviewee': 5,
            'text': 'wut',
            'score': 5
        }

        res = json.loads(self.client.post('http://localhost:8001/api/v1/reviews/create/', form_data, format='json').content.decode('utf-8'))

        self.assertEqual("error" in res, True)
        self.assertEqual(res["ok"], False)

        form_data = {
        	'reviewer': 4 # not enough data
        }

        res = json.loads(self.client.post('http://localhost:8001/api/v1/reviews/create/', form_data, format='json').content.decode('utf-8'))

        self.assertEqual("error" in res, True)
        self.assertEqual(res["ok"], False)


    def test_update(self):
        post_data = {'text': 'The guy texted me mean things after I returned the item'}
        response = self.client.post('http://models-api:8001/api/v1/reviews/7/', post_data, format='json')
        self.assertEquals(response.status_code, 200)

        string = response.content.decode('utf-8')
        response = json.loads(string)
        self.assertEquals(response['ok'], True)

        self.assertEquals(Review.objects.get(id=7).text, 'The guy texted me mean things after I returned the item')


    def test_update_fails(self):
        form_data = {'score': 7} # invalid score
        res = json.loads(self.client.post('http://localhost:8000/api/v1/reviews/7/', form_data, format='json').content.decode('utf-8'))
        self.assertEqual("error" in res, True)
        self.assertEqual(res["ok"], False)

        form_data = {'score': 2.5} # invalid score
        res = json.loads(self.client.post('http://localhost:8000/api/v1/reviews/7/', form_data, format='json').content.decode('utf-8'))
        self.assertEqual("error" in res, True)
        self.assertEqual(res["ok"], False)


    def test_delete(self):
        review = Review.objects.create(
        			reviewer=User.objects.get(id=8),
        			reviewee=User.objects.get(id=5),
        			text='foo bar',
        			score=5
                )

        num_reviews = Review.objects.count()
        response = self.client.delete('http://models-api:8001/api/v1/reviews/{}/delete/'.format(review.id))
        self.assertEquals(response.status_code, 200)
        string = response.content.decode('utf-8')
        response = json.loads(string)
        self.assertEquals(response['ok'], True)

        self.assertEquals(num_reviews, Review.objects.count() + 1)


    def test_delete_fails(self):
        res = json.loads(self.client.delete('http://localhost:8000/api/v1/reviews/100/delete/').content.decode('utf-8'))
        
        exp = json.loads(r"""{"error": "Review with id=100 not found", "ok": false}""")
        self.assertEqual(res, exp)


    #tearDown method is called after each test
    def tearDown(self):
        pass