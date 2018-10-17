from django.test import TestCase
from django.urls import reverse
from app.models import Review

class TestReviews(TestCase):
    #setUp method is called before each test in this class
    def setUp(self):
        pass #nothing to set up

    #tearDown method is called after each test
    def tearDown(self):
        pass #nothing to tear down