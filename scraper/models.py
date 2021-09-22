from django.db import models
from model_utils.models import TimeStampedModel
from myaccount.models import CustomUser
from twitter_data_extractor.settings.base import AUTH_USER_MODEL

from django.core.validators import MaxValueValidator
# validator for limit
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


def validate_limit(value):
    if value % 20 != 0:
        raise ValidationError(
            _('%(value)s is not an increment of 20 '),
            params={'value': value},
        )




class Job(TimeStampedModel):
    """ Input job"""
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="jobs")
    keyword = models.CharField(max_length=255, help_text="Search keyword")
    since = models.DateTimeField(help_text="Filter Tweets since date(Example: 2017-12-26 00:00:00).", null=True)
    until = models.DateTimeField(help_text="Filter Tweets sent until date(Example: 2017-12-27 00:00:00).", null=True)
    twitter_username = models.CharField(max_length=255, help_text="Twitter user's username", blank=True, null=True)
    limit = models.IntegerField(help_text="Number of Tweets to pull (Increments of 20)",
                                validators=[validate_limit])
    credits_required = models.IntegerField()
    LANG_CHOICES = (
        ("ar", "arabic"),
        ("en", "english"),
        ("hi", "hindi"),
        ("ml", "malayalam"),
    )

    language = models.CharField(choices=LANG_CHOICES, help_text="Tweet language", max_length=255)
    verified = models.BooleanField(help_text="Set to True to only show Tweets by _verified_ users")
    OUTPUT_CHOICES = (
        ("csv", "csv"),
        ("json", "json"),
    )
    output_type = models.CharField(choices=OUTPUT_CHOICES,
                                   help_text="Format in which you want to download the result",
                                   max_length=255, default="csv")

    def clean(self):
        if self.until is not None and self.since >= self.until:
            raise ValidationError('Please enter proper date (since date should be before until date).')
        super(Job, self).clean()

    def __str__(self):
        return f"{self.user}_{self.keyword}_{self.id}"


class Result(TimeStampedModel):
    """Result data"""
    job = models.OneToOneField(Job, on_delete=models.CASCADE, related_name="result")
    result_file = models.FileField(blank=True, upload_to='DataFiles/')

    def __str__(self):
        return f"{self.job.user}_{self.job}"

