import os

from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
set = os.environ.get("DJANGO_SETTINGS_MODULE", "myshop.settings.local")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', set)
app = Celery('myshop')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
