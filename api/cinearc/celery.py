import os
from celery import Celery

# Configuration Celery avec Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cinearc.settings')

app = Celery('cinearc')

# Charger les configurations de Celery depuis settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# Découverte automatique des tâches dans toutes les applications Django
app.autodiscover_tasks()
