from .base import *

import os

DEBUG = False

ALLOWED_HOSTS = ['twitter-data-extractor.herokuapp.com']

SECRET_KEY = os.environ['SECRET_KEY']
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
DEFAULT_FROM_EMAIL = os.environ['DEFAULT_FROM_EMAIL']

# heroku storage
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

import dj_database_url

prod_db = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(prod_db)

# django-paypal settings
PAYPAL_RECEIVER_EMAIL = os.environ.get('PAYPAL_RECEIVER_EMAIL')  # refers to the email used to create the PayPal myaccount

PAYPAL_TEST = True  # whether you want to use the live or sandbox myaccount
