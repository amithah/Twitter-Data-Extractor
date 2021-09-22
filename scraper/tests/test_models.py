from django.test import TestCase
from django.forms import ValidationError
from scraper.models import Job,Result
from myaccount.models import CustomUser,Profile
from datetime import datetime
from scraper.tasks import data_extract


class JobTest(TestCase):

    def setUp(self):
        self.user1= CustomUser.objects.create(username="Aamy",email="abcd@gmail.com")
        self.user2= CustomUser.objects.create(username="Nithin",email="xyz@gmail.com")
        self.job1= Job.objects.create(keyword="covid",
        user = self.user1,
        since = "2017-12-26 00:00:00",
        until =  "2017-12-27 00:00:00",
        limit = 20,
        credits_required=0,
        language = "en",
        verified = "True",
        output_type = "csv")

        self.job2= Job.objects.create(keyword="covid",
        user = self.user1,
        since = "2017-12-27 00:00:00",
        until =  "2017-12-26 00:00:00",
        limit = 20,
        credits_required=0,
        language = "en",
        verified = "True",
        output_type = "csv")
       


    def test_model_str(self):
        self.assertEqual(str(self.job1),"Aamy_covid_1")
    
    def test_since_date_error(self):
        with self.assertRaises(ValidationError) as er:
            self.job2.full_clean()
        self.assertTrue(er,'Please enter proper date (since date should be before until date' )
    def test_tweets_extracted(self):
        user= CustomUser.objects.create(username="user1",email="abcde@gmail.com")
        job= Job.objects.create(keyword="covid",
        user = user,
        since = datetime.strptime("2017-07-12 00:00:00","%Y-%m-%d %H:%M:%S"),
        until = datetime.strptime("2017-08-12 00:00:00","%Y-%m-%d %H:%M:%S"),
        limit = 20,
        credits_required=0,
        language = "en",
        verified = "True",
        output_type = "csv")
        task=data_extract.delay(job.id,user.id)
        task.get()
        result= Result.objects.get(job=job)
        self.assertEqual(task.status, 'SUCCESS')
        self.assertEqual(str(result),"Aamy_covid_1")
       


