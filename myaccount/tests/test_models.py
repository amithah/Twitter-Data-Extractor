from django.test import TestCase
from myaccount.models import CustomUser,Profile,update_profile_signal


class TestModels(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = CustomUser.objects.create(username="User11",email="abcd@gmail.com")
        cls.user2 = CustomUser.objects.create(username="User21",email="abc@gmail.com")
        
    def test_user_str(self):
        self.assertEqual(str(self.user1),"User11")

    def test_profile_str(self):
        profile= self.user2.profile
        self.assertEqual(str(profile),"User21")
