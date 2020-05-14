from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

class HomeViewTest(TestCase):
    def test_home(self):
        client=Client()
        response=client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')