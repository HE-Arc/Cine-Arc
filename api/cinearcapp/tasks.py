import requests
from datetime import datetime
from celery import shared_task
from cinearcapp.models import Movie

TMDB_API_KEY = "a659f5bf4363e91056c093da0b3c3372"
TMDB_NOW_PLAYING_URL = "https://api.themoviedb.org/3/movie/now_playing"


@shared_task
def fetch_and_store_movies():
    """Récupère les films actuellement en salle et les stocke en BD."""
    try:
        params = {
            "api_key": TMDB_API_KEY,
            "language": "fr-FR",
            "page": 1,
            "region": "CH"
        }
        response = requests.get(TMDB_NOW_PLAYING_URL, params=params)
        response.raise_for_status()
        data = response.json()

        if 'results' not in data:
            raise ValueError("Clé 'results' absente dans la réponse de TMDB")

        movies = data['results'][:10]

        for movie in movies:
            title = movie.get("title", "Titre Inconnu")
            synopsis = movie.get("overview", "")[:100]
            duration = movie.get("runtime") or 90
            type_movie = ", ".join(str(g) for g in movie.get("genre_ids", []))
            release_date = movie.get("release_date", None)
            picture_url = f"https://image.tmdb.org/t/p/w500{movie.get('poster_path')}" if movie.get("poster_path") else ""
            rating = int(movie.get("vote_average", 0))
            api_id = movie.get("id")

            if release_date:
                try:
                    release_date = datetime.strptime(release_date, "%Y-%m-%d").date()
                except ValueError:
                    release_date = None

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

        return f"{len(movies)} films ajoutés avec succès"

    except requests.exceptions.RequestException as e:
        return f"Erreur de requête à TMDB : {str(e)}"
    except ValueError as e:
        return f"Erreur de format de données : {str(e)}"
    except Exception as e:
        return f"Erreur inattendue : {str(e)}"