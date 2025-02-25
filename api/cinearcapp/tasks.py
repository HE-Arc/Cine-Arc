from celery import shared_task
from .models import Movie
from datetime import datetime
import requests
import logging
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from django.utils.timezone import now
import json

logger = logging.getLogger(__name__)

TMDB_API_KEY = 'a659f5bf4363e91056c093da0b3c3372'
TMDB_NOW_PLAYING_URL = 'https://api.themoviedb.org/3/movie/now_playing'


@shared_task
def fetch_and_add_movies():
    logger.info("La tâche fetch_and_add_movies a démarré.")
    print("La tâche fetch_and_add_movies a démarré.")

    try:
        params = {
            'api_key': TMDB_API_KEY,
            'language': 'fr-FR',
            'page': 1,
            'region': 'CH'
        }
        response = requests.get(TMDB_NOW_PLAYING_URL, params=params)
        response.raise_for_status()
        logger.info(f"Réponse API : {response.status_code}")
        movies = response.json().get('results', [])
        logger.info(f"{len(movies)} films récupérés.")

        count_added = 0
        for movie in movies:
            title = movie.get('title', 'Titre Inconnu')
            logger.info(f"Traitement du film : {title}")
            synopsis = movie.get('overview', '')[:100]
            duration = movie.get('runtime') or 90
            type_movie = ', '.join(str(g) for g in movie.get('genre_ids', []))
            release_date = datetime.strptime(movie.get('release_date', '2000-01-01'), "%Y-%m-%d").date()
            picture_url = f"https://image.tmdb.org/t/p/w500{movie.get('poster_path')}" if movie.get('poster_path') else ''
            rating = int(movie.get('vote_average', 0))
            api_id = movie.get('id')

            if not Movie.objects.filter(api_id=api_id).exists():
                Movie.objects.create(
                    title=title,
                    synopsis=synopsis,
                    duration=duration,
                    type=type_movie,
                    release_date=release_date,
                    picture_url=picture_url,
                    rating=rating,
                    api_id=api_id
                )
                count_added += 1
                logger.info(f"Film ajouté : {title}")
            else:
                logger.info(f"Film déjà existant : {title}")

        return f"{count_added} films ajoutés avec succès."

    except Exception as e:
        logger.error(f"Erreur lors de l'exécution : {str(e)}", exc_info=True)
        raise e


def schedule_fetch_and_add_movies():
    """Crée ou met à jour une tâche planifiée tous les samedis à 6h du matin."""
    schedule, _ = CrontabSchedule.objects.get_or_create(
        minute='0',  
        hour='6',
        day_of_week='6',
        day_of_month='*',
        month_of_year='*',
    )

    PeriodicTask.objects.update_or_create(
        name='Update movies from TMDB every Saturday at 6 AM',
        defaults={
            'crontab': schedule,
            'task': 'cinearcapp.tasks.fetch_and_add_movies',
            'enabled': True,
            'start_time': now(),
            'kwargs': json.dumps({})
        }
    )
