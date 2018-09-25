import os

from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
set = os.environ.get("DJANGO_SETTINGS_MODULE", "myshop.settings.local")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', "myshop.settings.pro")
app = Celery('myshop', broker="amqp://ahsjsxrt:i3jAz8LoqtzxFoyd3wytZ7JUGRNCVG19@termite.rmq.cloudamqp.com/ahsjsxrt")
app.config_from_object('django.conf:settings', namespace="CELERY")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
