from .base import *

DEBUG = True

# DATABASES
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'digied',
        'USER': 'postgres',
        'PASSWORD': 'reductionism',
    }
}
# paystack
PAYSTACK_SECRET_KEY = "sk_test_54b7b02a10391dee8a2ed4a942e63c6c185fd3dd"
PAYSTACK_PUBLIC_KEY = "pk_test_6d19b1035287fb78ec85b8eabb68b8aef75771cf"

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'