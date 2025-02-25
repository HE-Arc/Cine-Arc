from django_celery_beat.models import PeriodicTask, CrontabSchedule
from django.utils.timezone import now

def run_task_schedule(sender, **kwargs):
    """Crée ou met à jour une tâche planifiée tous les samedis à 6h du matin."""
    schedule, _ = CrontabSchedule.objects.get_or_create(
        minute='0',           # À 0 minute
        hour='6',             # À 6 heures du matin
        day_of_week='6',      # Le samedi (0=dimanche, 6=samedi)
        day_of_month='*',     # Tous les jours du mois
        month_of_year='*',    # Tous les mois
    )

    PeriodicTask.objects.update_or_create(
        name='Update movies from TMDB every Saturday at 6 AM',
        defaults={
            'crontab': schedule,
            'task': 'cinearcapp.tasks.fetch_and_add_movies',
            'enabled': True,
            'start_time': now(),
        }
    )
