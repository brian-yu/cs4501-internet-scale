from django.test import TestCase, Client
from app.models import Item, User, Borrow, Review, Authenticator
import urllib.request
import urllib.parse
import json

class AuthenticatorTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_authenticator_login(self):
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
        form_data = {
            'email': 'obama@usa.gov',
            'password': 'ilovemichellexoxo69',
        }
        res = json.loads(self.client.post('http://localhost:8000/api/v1/login/', form_data, format='json').content.decode('utf-8'))
        #exp = json.loads(r"""{"ok": true, "result": {"authenticator": "3118d398ee4b3d5a240d15f8d8ff3960f6f73bbb506be282a67e21eeac701d95"}}""")
        self.assertEqual('authenticator' in res['result'], True)
