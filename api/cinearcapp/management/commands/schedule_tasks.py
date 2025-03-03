from django.core.management.base import BaseCommand
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from django.utils.timezone import now
import json


class Command(BaseCommand):
    help = "Ajoute une tâche planifiée pour récupérer les films en salle avec Crontab et start_time."

    def handle(self, *args, **kwargs):
        start_time = now()

        schedule, created = CrontabSchedule.objects.get_or_create(
            minute="0",  # À la minute 0
            hour="6",     # À 6h du matin
            day_of_week="6",  # Le samedi (0 = dimanche, 6 = samedi)
            day_of_month="*",  # Chaque jour du mois
            month_of_year="*",  # Chaque mois
        )

        # Nom de la tâche
        task_name = "fetch_movies_crontab"

        # Vérifie si la tâche existe déjà et met à jour ou crée
        task, created = PeriodicTask.objects.update_or_create(
            name=task_name,
            defaults={
                "crontab": schedule,
                "task": "cinearcapp.tasks.fetch_and_store_movies",
                "args": json.dumps([]),
                "kwargs": json.dumps({}),
                "enabled": True,
                "start_time": start_time,
                "last_run_at": None,
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f"Tâche '{task_name}' ajoutée avec succès. Elle commencera à {start_time}."))
        else:
            self.stdout.write(self.style.WARNING(f"Tâche '{task_name}' mise à jour. Elle commencera à {start_time}."))
