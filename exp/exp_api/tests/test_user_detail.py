from django.test import TestCase, Client
import json

class TestUsers(TestCase):

    def setUp(self):
        self.client = Client()

    def test_user_exists(self):
        recv_json = self.client.get(
            '/api/v1/users/4/'
            ).content.decode("utf-8")
        recv_dict = json.loads(recv_json)
        
        self.assertEqual(exp_json, recv_dict)