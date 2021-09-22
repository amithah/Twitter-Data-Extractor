from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import EmailValidator
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.dispatch import receiver
from django.db.models.signals import post_save

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


class CustomUser(AbstractUser):
    """ Custom user model"""
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        max_length=150,
        unique=True,
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
        validators=[username_validator],
        error_messages={
            'unique': "A user with that username already exists.",
        },
    )
    password1 = models.CharField(max_length=32, null=True)
    password2 = models.CharField(max_length=32, null=True)
    email = models.EmailField(unique=True, validators=[EmailValidator])

    # add additional fields in here

    def __str__(self):
        return self.username


class Profile(models.Model):
    """ User profile"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="profile")
    user_credit = models.IntegerField(default=0)
    job_count = models.IntegerField(default=0)
    job_limit=models.IntegerField(default=5)
    PLAN_CHOICES = (
        ("fr", "free"),
        ("nn","none"),
        ("ot", "onetime"),
        ("mn", "monthly"),
        ("yr", "yearly"),
    )
    plan = models.CharField(choices=PLAN_CHOICES, default="fr", max_length=255)


    def __str__(self):
        return self.user.username


@receiver(post_save, sender=CustomUser)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        # notify admin when new user signup
        subject, from_email, to = 'User login', 'amithah.nithin@gmail.com', 'amithah.nithin@gmail.com'
        html_content = render_to_string('myaccount/email.html', {'user':instance})  # render with dynamic value
        text_content = strip_tags(html_content)  # Strip the html tag. So people can see the pure text at least.

        # create the email, and attach the HTML version as well.
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    instance.profile.save()
