import os
import django
import requests
from datetime import datetime

# Configuration de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cinearc.settings')
django.setup()

from cinearcapp.models import Movie

# Clé API TMDB et URL
TMDB_API_KEY = 'a659f5bf4363e91056c093da0b3c3372'
TMDB_NOW_PLAYING_URL = 'https://api.themoviedb.org/3/movie/now_playing'


def fetch_now_playing_movies(api_key, number_of_movies=10):
    """Récupère les films actuellement en salle (jusqu'à 10)."""
    params = {
        'api_key': api_key,
        'language': 'fr-FR',
        'page': 1,
        'region': 'CH'
    }
    response = requests.get(TMDB_NOW_PLAYING_URL, params=params)
    response.raise_for_status()
    data = response.json()
    return data['results'][:number_of_movies]


def add_movies_to_db(movies):
    """Ajoute les films récupérés dans la base de données."""
    for movie in movies:
        try:
            title = movie.get('title', 'Titre Inconnu')
            synopsis = movie.get('overview', '')[:100]  # Limité à 100 caractères
            duration = movie.get('runtime') or 90  # Valeur par défaut si manquante
            type_movie = ', '.join(str(g) for g in movie.get('genre_ids', []))
            release_date = datetime.strptime(movie.get('release_date', '2000-01-01'), "%Y-%m-%d").date()
            picture_url = f"https://image.tmdb.org/t/p/w500{movie.get('poster_path')}" if movie.get('poster_path') else ''
            rating = int(movie.get('vote_average', 0))
            api_id = movie.get('id')

            # Vérification de l'existence avant insertion
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
                print(f"Film ajouté : {title}")
            else:
                print(f"Film déjà présent : {title}")

        except Exception as e:
            print(f"Erreur lors de l'ajout du film {title}: {str(e)}")


def main():
    print("Récupération des films en cours...")
    try:
        movies = fetch_now_playing_movies(TMDB_API_KEY)
        print(f"{len(movies)} films récupérés. Ajout en base de données...")
        add_movies_to_db(movies)
        print("Population de la base terminée.")
    except Exception as e:
        print(f"Une erreur est survenue : {str(e)}")


if __name__ == "__main__":
    main()
