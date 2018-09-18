from .base import *
import django_heroku

DEBUG = True
ALLOWED_HOSTS = ['dlearn.tk', 'www.dlearn.tk', "dlearn.herokuapp.com", "www.dlearn.herokuapp.com"]

ADMINS = (
('Samuel Taiwo', 'taiwogabrielsamuel@gmail.com'),
)


SECRET_KEY = os.environ.get("SECRET_KEY", "*pgdt3h3ta7-i7!_*^(*&()*)*fdvsappmy0$f(v3any06v&1cw4c!gh%1x)@")
# DATABASES
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': "ec2-107-22-221-60.compute-1.amazonaws.com",
        'NAME': 'd6fk0t2sq5ul7i',
        'USER': 'yvwgbarytxgwpa',
        'PASSWORD': os.environ.get("DATABASE_PWD"),
    }
}
# paystack
PAYSTACK_SECRET_KEY = os.environ.get("PAYSTACK_SECRET_KEY")
PAYSTACK_PUBLIC_KEY = os.environ.get("PAYSTACK_PUBLIC_KEY")

# Email settings
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'noreply@gmail.com'
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_PORT = 587
EMAIL_USE_TLS = True

django_heroku.settings(locals())
# Security Settings

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
# SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = "DENY"

# veOFdNEXM0ugmxJsgauaKrH1 = elasticsearch password
# username = elastic

# elasticsearch settings
FOUNDELASTICSEARCH_URL = os.environ.get("FOUNDELASTICSEARCH_URL", "localhost")
HTTP_AUTH = os.environ.get("elastic:veOFdNEXM0ugmxJsgauaKrH1")