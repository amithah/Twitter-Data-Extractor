"""Account confirmatio token
(https://dev.to/coderasha/create-advanced-user-sign-up-view-in-django-step-by-step-k9m)
"""
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp)
        )


account_activation_token = AccountActivationTokenGenerator()