from .base import *
import django_heroku

DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY', 'ffa-e&09jjk)&^$()&rpe-6sp1)_$m49widsj934-0e]%^&!+_)(*&|/.>@!~`415_$1x_js6@syk^0n=l@4==(#xhgx3')


ADMINS = (
    ('Samuel Taiwo', 'taiwogabrielsamuel@gmail.com'),
)

ALLOWED_HOSTS = ['dlearn.tk', 'www.dlearn.tk', 'dlearn.herokuapp.com']

# DATABASES
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': 'ec2-107-22-221-60.compute-1.amazonaws.com',
        'NAME': 'd6fk0t2sq5ul7i',
        'USER': 'yvwgbarytxgwpa',
        'PASSWORD': 'f39e5fdfbfff04af5fef9d8435564bdc8f2e2f3fe90e060b095b8d2616c316d5',
    }
}

SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = True
X_FRAME_OPTIONS = "DENY"

# EMAIL SETTINGS
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'taiwogabrielsamuel@gmail.com'
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True


# MEDIA STORAGE SETTINGS
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# AWS_ACCESS_KEY_ID = "AKIAJIJRNDCCJNBY7COQ"
# AWS_SECRET_ACCESS_KEY = "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"
# AWS_STORAGE_BUCKET_NAME = "digied"
# AWS_AUTO_CREATE_BUCKET = True

# paystack
PAYSTACK_SECRET_KEY = "sk_live_ae71ccab6d383502178aa64b9dd7855d73a2d6a7"
PAYSTACK_PUBLIC_KEY = "pk_live_6b5b150f50bf823f4a0056ebb9aca560d5d7626b"

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

django_heroku.settings(locals())

import dj_database_url

db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)
DATABASES['default']['CONN_MAX_AGE'] = 500