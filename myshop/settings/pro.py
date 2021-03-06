import django_heroku
from .base import *

DEBUG = False
ALLOWED_HOSTS = ['dlearn.tk', 'www.dlearn.tk', "dlearn.herokuapp.com",
                 "www.dlearn.herokuapp.com"]

ADMINS = (
('Samuel Taiwo', 'taiwogabrielsamuel@gmail.com'),
)


SECRET_KEY = os.environ.get("SECRET_KEY", "*pgdt3h3ta7-i7!_*^(*&()*)*fdvsappmy0$f(v3any06v&1cw4c!gh%1x)@")

# DATABASES
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': "ec2-54-83-27-165.compute-1.amazonaws.com",
        'NAME': 'd8ofac7claoi38',
        'USER': 'pbopyrzbcncpra',
        'PASSWORD': os.environ.get("DATABASE_PWD"),
    }
}
# paystack
PAYSTACK_SECRET_KEY = os.environ.get("PAYSTACK_SECRET_KEY")
PAYSTACK_PUBLIC_KEY = os.environ.get("PAYSTACK_PUBLIC_KEY")

# Email settings
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'snpet.hub@gmail.com'
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = "order@dlearn.com"

django_heroku.settings(locals())

# Security Settings
CORS_REPLACE_HTTPS_REFERER = True
HOST_SCHEME = "https://"
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

SECURE_HSTS_SECONDS = 1000000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

SECURE_FRAME_DENY = True
X_FRAME_OPTIONS = "DENY"

SECURE_REDIRECT_EXEMPT = [r"^http://ebook-dl.com/pictures/books/"]

SITE_ID = 2

# elasticsearch settings
FOUNDELASTICSEARCH_URL = os.environ.get("FOUNDELASTICSEARCH_URL", "localhost")
HTTP_AUTH = os.environ.get("HTTP_AUTH", "elastic:veOFdNEXM0ugmxJsgauaKrH1")

CELERY_BROKER_URL = os.environ.get("CLOUDAMQP_URL")

CELERY_BROKER_POOL_LIMIT = 1
CELERY_IMPORTS = ('orders.tasks',)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

ROBOTS_SITEMAP_URLS = [
    'https://dlearn.tk/sitemap.xml',
]

SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'METHOD': 'oauth2',
        'SCOPE': ['email', 'public_profile', 'user_friends'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'INIT_PARAMS': {'cookie': True},
        'FIELDS': [
            'email',
            'name',
            'first_name',
            'last_name',
        ],
        'EXCHANGE_TOKEN': True,
        'VERIFIED_EMAIL': False,
        
    }
}
