from django.test import TestCase
from django.urls import reverse
from app.models import User, Item, Borrow, Review, Recommendation
import json

class TestRecommendations(TestCase):

    fixtures = ['db.json']
    
    #setUp method is called before each test in this class
    def setUp(self):
        post_data = {
            'item1_id': 9,
            'item2_id': 12,
        }

        response = self.client.post('http://models-api:8001/api/v1/recommendations/create/', post_data, format='json')
        # self.assertEquals(response.status_code, 200)

        # string = response.content.decode('utf-8')
        # response = json.loads(string)
        # self.assertEquals(response['ok'], True)
        # pass

    def test_get_success(self):
        response = self.client.get('http://localhost:8001/api/v1/recommendations/9/')
        string = response.content.decode('utf-8')
        response = json.loads(string)['result']

        self.assertEquals(response[0]['id'], 12)

        response = self.client.get('http://localhost:8001/api/v1/recommendations/12/')
        string = response.content.decode('utf-8')
        response = json.loads(string)['result']

        self.assertEquals(response[0]['id'], 9)

    #tearDown method is called after each test
    def tearDown(self):
        pass