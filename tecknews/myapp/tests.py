from django.test import TestCase
from django.test import Client
from rest_framework.test import APIRequestFactory
from django.urls import include, path, reverse
from rest_framework.test import APITestCase, URLPatternsTestCase
from rest_framework import status
# Create your tests here.
from django.core.cache import cache


class AnimalTestCase(TestCase):
    def setUp(self):
        # setup_test_environment()
        pass
        # Animal.objects.create(name="lion", sound="roar")
        # Animal.objects.create(name="cat", sound="meow")

    def test_animals_can_speak(self):
        cache.clear()
        # client = Client()
        response = self.client.get('/Newsposts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertGreater(len(response.data), 0)
    
    def test_create_account2(self):
        cache.clear()
    
        response = self.client.post('/Newsposts/',{
                                                    "title": "lll",
                                                    "content": "ppppp",
                                                    "tag": "dlkrf", 
                                                    "resource": ";[[]]]]"
                                                    }, format='json')
        # print(response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


# class AccountTests(APITestCase, URLPatternsTestCase):
#     urlpatterns = [
#         path('', include('tecknews.urls')),
#     ]

#     def test_create_account(self):
#         """
#         Ensure we can create a new account object.
#         """
#         # url = reverse('Newsposts')
#         response = self.client.get('/Newsposts/', format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         print(response.content)
#         # self.assertGreater(len(response.data), 0)
#     def test_create_account2(self):
#         """
#         Ensure we can create a new account object.
#         """
#         # url = reverse('Newsposts')
#         response = self.client.post('/Newsposts/',{
#                                                     "title": "lll",
#                                                     "content": "ppppp",
#                                                     "tag": "dlkrf", 
#                                                     "resource": ";[[]]]]"
#                                                     }, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)