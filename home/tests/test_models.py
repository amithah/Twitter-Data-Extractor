from django.test import TestCase
from home.models import Contact

from django.core import mail


class ContactTest(TestCase):
    def test_model_str(self):
        name = Contact.objects.create(name="Aamy")
        self.assertEqual(str(name),"Aamy")
