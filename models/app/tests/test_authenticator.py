from django.test import TestCase, Client
from app.models import Item, User, Borrow, Review, Authenticator
import urllib.request
import urllib.parse
import json

class AuthenticatorTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_authenticator_login():
        form_data = {
            'first_name': 'Barack',
            'last_name': 'Obama',
            'email': 'obama@usa.gov',
            'overview': 'I\'m President, bitch!',
            'zip_code': '22903',
            'phone_number': '1234567890',
            'password': 'ilovemichellexoxo69'
        }
        res = json.loads(self.client.post('http://localhost:8000/api/v1/users/create/', form_data, format='json').content.decode('utf-8'))
        res = json.loads(self.client.post('http://localhost:8000/api/v1/users/login/'))
