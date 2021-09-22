from django.test import TestCase
from home.views import home
from django.urls import resolve
from home.models import Contact

class HomePageTest(TestCase):

    def test_home_page_returns_correcthtml(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response,'home/index.html')

    def test_home_can_have_a_post_request(self):
        response = self.client.post('/', data={'name':'amy','email':'abcd@gmail.com','subject':'abcd','message':"hi"})
        self.assertEqual(Contact.objects.count(),1)

    def test_home_redirects_after_post(self):
        response = self.client.post('/', data={'name':'amy','email':'abcd@gmail.com','subject':'abcd','message':"hi"})
        self.assertEqual(response.status_code, 302)
