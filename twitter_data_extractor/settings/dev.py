from .base import *

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']

SECRET_KEY = os.environ.get('SECRET_KEY', default='ku&rmhu1ag6*')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL ')

# django-paypal settings
PAYPAL_RECEIVER_EMAIL = os.environ.get('PAYPAL_RECEIVER_EMAIL')  # refers to the email used to create the PayPal
# myaccount.

PAYPAL_TEST = True  # whether you want to use the live or sandbox myaccount
