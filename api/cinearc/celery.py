import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cinearc.settings')

# Create an instance of the Celery application with the name 'cinearc'.
app = Celery('cinearc')

# Load Celery configuration from Django's settings.py file.
# The 'namespace' argument ensures that only settings prefixed with 'CELERY_' are used.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Automatically discover tasks defined in all installed Django apps.
# This allows Celery to find and register tasks without explicitly listing them.
app.autodiscover_tasks()
