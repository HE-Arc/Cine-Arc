import os
import requests
from datetime import datetime
from celery import shared_task
from dotenv import load_dotenv
from cinearcapp.models import Movie

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")

if not TMDB_API_KEY:
    raise ValueError("ERREUR: La clé API TMDB est manquante ! Vérifiez votre fichier .env")

TMDB_NOW_PLAYING_URL = "https://api.themoviedb.org/3/movie/now_playing"
TMDB_MOVIE_DETAILS_URL = "https://api.themoviedb.org/3/movie/{movie_id}"
TMDB_GENRES_URL = "https://api.themoviedb.org/3/genre/movie/list"

def fetch_movie_runtime(movie_id):
    """Récupère la durée du film en minutes via l'API TMDB"""
    try:
        url = TMDB_MOVIE_DETAILS_URL.format(movie_id=movie_id)
        response = requests.get(url, params={"api_key": TMDB_API_KEY, "language": "fr-FR"})
        response.raise_for_status()
        data = response.json()
        return data.get("runtime", 90)  # Si la durée n'est pas trouvée, utiliser 90 min par défaut
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération de la durée pour le film {movie_id} : {e}")
        return 90  # Valeur par défaut en cas d'erreur

def fetch_genres():
    """Récupère la liste des genres depuis TMDB et les stocke dans un dictionnaire."""
    try:
        response = requests.get(TMDB_GENRES_URL, params={"api_key": TMDB_API_KEY, "language": "fr-FR"})
        response.raise_for_status()
        genres_data = response.json()
        
        # Transformer la liste des genres en un dictionnaire {id: nom}
        genre_dict = {genre["id"]: genre["name"] for genre in genres_data.get("genres", [])}
        return genre_dict

    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération des genres : {e}")
        return {}
    

@shared_task
def fetch_and_store_movies():
    """Récupère les films actuellement en salle et les stocke en BD."""
    try:
        # Récupérer la correspondance ID -> Nom des genres
        genre_mapping = fetch_genres()

        if not genre_mapping:
            print("Attention : aucun genre récupéré, les films seront enregistrés avec des IDs au lieu des noms.")

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
            api_id = movie.get("id")
            title = movie.get("title", "Titre Inconnu")
            synopsis = movie.get("overview", "")[:500]
            genre_ids = movie.get("genre_ids", [])

            duration = fetch_movie_runtime(api_id)

            # Convertir les IDs en noms de genres
            type_movie = ", ".join(genre_mapping.get(g, f"Genre inconnu ({g})") for g in genre_ids)

            release_date = movie.get("release_date", None)
            picture_url = f"https://image.tmdb.org/t/p/w500{movie.get('poster_path')}" if movie.get("poster_path") else ""
            rating = int(movie.get("vote_average", 0))

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
                print(f"Film ajouté : {title} ({type_movie})")
            else:
                print(f"Film déjà présent : {title}")

        return f"{len(movies)} films ajoutés avec succès"

    except requests.exceptions.RequestException as e:
        return f"Erreur de requête à TMDB : {str(e)}"
    except ValueError as e:
        return f"Erreur de format de données : {str(e)}"
    except Exception as e:
        return f"Erreur inattendue : {str(e)}"
