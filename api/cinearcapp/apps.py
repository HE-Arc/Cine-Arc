from django.apps import AppConfig
from django.db.models.signals import post_migrate

class CinearcappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cinearcapp'

    def ready(self):
        # Import différé pour éviter l'erreur "Apps aren't loaded yet"
        from django.db.models.signals import post_migrate
        from .signals import run_task_schedule 
        post_migrate.connect(run_task_schedule, sender=self)