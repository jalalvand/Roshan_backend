from django.test import TestCase
from django.test import Client
from rest_framework import status
from django.core.cache import cache

# Create your tests here.


class AnimalTestCase(TestCase):
    def setUp(self):

        pass

    def test_animals_can_speak(self):
        cache.clear()
        # client = Client()
        response = self.client.get('/scrape/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertGreater(len(response.data), 0)
