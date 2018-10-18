from django.test import TestCase, Client
import json

class TestUsers(TestCase):
    fixtures = ["db.json"]

    def setUp(self):
        self.client = Client()

    def test_get_user_success(self):
        recv_json = self.client.get(
            'http://localhost:8000/api/v1/users/4/'
            ).content.decode("utf-8")
        recv_dict = json.loads(recv_json)
        self.assertEqual(recv_dict['result']['user']['first_name'], 'Brian')

        # Test that user items are included
        self.assertEqual('items' in recv_dict['result'], True) 

        # Test that reviews of a user are included
        self.assertEqual('received_reviews' in recv_dict['result'], True)

    def test_get_user_fail(self):
        res = json.loads(self.client.get(
            'http://localhost:8000/api/v1/users/100/'
            ).content.decode("utf-8"))
        expected = json.loads(
            r"""{"error": "User with id=100 not found", "ok": false}"""
            )
        self.assertEqual(res, expected)

    def test_create_user_success(self):
        form_data = {
            'first_name': 'Barack',
            'last_name': 'Obama',
            'email': 'obama@usa.gov',
            'overview': 'I\'m President, bitch!',
            'zip_code': '22903',
            'phone_number': '1234567890'
        }
        res = json.loads(self.client.post('http://localhost:8000/api/v1/users/create/', form_data, format='json').content.decode('utf-8'))

        exp = json.loads(r"""{"result": {"first_name": "Barack", "last_name": "Obama", "email": "obama@usa.gov", "zip_code": "22903", "borrower_rating_total": 0, "borrower_rating_count": 0, "lender_rating_count": 0, "phone_number": "1234567890", "id": 13, "overview": "I'm President, bitch!", "lender_rating_total": 0}, "ok": true}""")
        self.assertEqual(res, exp)

    def test_create_user_fail(self):
        form_data = {
            'first_name': 'This',
            'last_name': 'Fails'
        }

        res = json.loads(self.client.post('http://localhost:8000/api/v1/users/create/', form_data, format='json').content.decode('utf-8'))

        self.assertEqual("error" in res, True)
        self.assertEqual(res["ok"], False)

    def test_update_user_success(self):
        form_data = {'overview': 'i love writing tests'}
        res = json.loads(self.client.post('http://localhost:8000/api/v1/users/4/', form_data, format='json').content.decode('utf-8'))
        exp = json.loads(r"""{"ok": true, "result": {"last_name": "Yu", "borrower_rating_total": 0, "lender_rating_total": 0, "borrower_rating_count": 0, "email": "bry4xm@virginia.edu", "id": 4, "zip_code": "22903", "overview": "i love writing tests", "lender_rating_count": 0, "phone_number": "", "first_name": "Brian"}}""")
        self.assertEqual(res, exp)

    def test_update_user_fail(self):
        form_data = {'overview': 'i love writing tests'}
        res = json.loads(self.client.post('http://localhost:8000/api/v1/users/100/', form_data, format='json').content.decode('utf-8'))
        
        exp = json.loads(r"""{"error": "User with id=100 not found", "ok": false}""")
        self.assertEqual(res, exp)

    def test_delete_user_success(self):
        res = json.loads(self.client.delete('http://localhost:8000/api/v1/users/4/delete/').content.decode('utf-8'))
        
        exp = json.loads(r"""{"ok": true}""")
        self.assertEqual(res, exp)

        get = json.loads(self.client.get('http://localhost:8000/api/v1/users/4/').content.decode('utf-8'))
        get_exp = json.loads(r"""{"error": "User with id=4 not found", "ok": false}""")
        self.assertEqual(get, get_exp)

    def test_delete_user_fail(self):
        res = json.loads(self.client.delete('http://localhost:8000/api/v1/users/100/delete/').content.decode('utf-8'))
        
        exp = json.loads(r"""{"error": "User with id=100 not found", "ok": false}""")
        self.assertEqual(res, exp)