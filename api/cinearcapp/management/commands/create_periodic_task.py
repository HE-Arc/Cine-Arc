from django.core.management.base import BaseCommand
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from django.utils.timezone import now


class Command(BaseCommand):
    help = 'Crée une tâche planifiée pour mettre à jour les films tous les samedis à 6h du matin.'

    def handle(self, *args, **kwargs):
        schedule, _ = CrontabSchedule.objects.get_or_create(
            minute='0',
            hour='6',
            day_of_week='6',
            day_of_month='*',
            month_of_year='*',
        )
        task, created = PeriodicTask.objects.update_or_create(
            name='Update movies from TMDB every Saturday at 6 AM',
            defaults={
                'crontab': schedule,
                'task': 'cinearcapp.tasks.fetch_and_add_movies',
                'enabled': True,
                'start_time': now(),
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS('Tâche planifiée créée avec succès !'))
        else:
            self.stdout.write(self.style.SUCCESS('Tâche planifiée mise à jour avec succès !'))
