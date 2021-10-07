from .base import *
import os

DEBUG = False

ALLOWED_HOSTS = ['twitter-data-extractor.herokuapp.com',
                 '0.0.0.0', 'localhost',
                 '.ec2-3-83-139-94.compute-1.amazonaws.com','3.83.139.94']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv("DB_NAME"),
        'USER': os.getenv("DB_USER"),
        'PASSWORD': os.getenv("DB_PWD"),
        'HOST': os.getenv("DB_HOST"),
        'PORT': os.getenv("DB_PORT"),
    }
}


SECRET_KEY = os.environ['SECRET_KEY']
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
DEFAULT_FROM_EMAIL = os.environ['DEFAULT_FROM_EMAIL']



# django-paypal settings
PAYPAL_RECEIVER_EMAIL = os.environ.get('PAYPAL_RECEIVER_EMAIL')  # refers to the email used to create the PayPal myaccount

PAYPAL_TEST = True  # whether you want to use the live or sandbox myaccount
