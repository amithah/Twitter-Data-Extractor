from django.db import models
from model_utils.models import TimeStampedModel
from django.db import models
from django.core.validators import EmailValidator


class Contact(TimeStampedModel):
    """ Contact model"""
    name = models.CharField(max_length=255)
    email = models.EmailField(validators=[EmailValidator])
    subject = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return self.name
