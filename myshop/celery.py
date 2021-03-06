import os

from celery import Celery
from celery import task
from django.conf import settings

# set the default Django settings module for the 'celery' program.
set = os.environ.get("DJANGO_SETTINGS_MODULE", "myshop.settings.local")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', "myshop.settings.pro")
app = Celery('myshop')
app.config_from_object(settings, namespace="CELERY")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
