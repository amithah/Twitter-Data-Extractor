from django.db import models
from scraper.models import Job
from myaccount.models import CustomUser
from model_utils.models import TimeStampedModel


class Payment(TimeStampedModel):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE, related_name="payment")
    credits_added= models.IntegerField(default=0)
    status = models.BooleanField(default="False")

    def __str__(self):
        return f"{self.user}, {self.credits_added}, {self.status},{self.credits_added}"
