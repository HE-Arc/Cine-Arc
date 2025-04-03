import os
import requests
from datetime import datetime
from celery import shared_task
from dotenv import load_dotenv
from cinearcapp.models import Movie

# Load environment variables from the .env file
load_dotenv()

# Retrieve the TMDB API key from the environment variables
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

# Raise an error if the API key is missing
if not TMDB_API_KEY:
    raise ValueError("ERROR: TMDB API key is missing! Check your .env file")

# Define TMDB API endpoints
TMDB_NOW_PLAYING_URL = "https://api.themoviedb.org/3/movie/now_playing"
TMDB_MOVIE_DETAILS_URL = "https://api.themoviedb.org/3/movie/{movie_id}"
TMDB_GENRES_URL = "https://api.themoviedb.org/3/genre/movie/list"

def fetch_movie_runtime(movie_id):
    """
    Fetch the runtime of a movie in minutes using the TMDB API.
    If the runtime is not found, a default value of 90 minutes is used.
    """
    try:
        url = TMDB_MOVIE_DETAILS_URL.format(movie_id=movie_id)
        response = requests.get(url, params={"api_key": TMDB_API_KEY, "language": "fr-FR"})
        response.raise_for_status()
        data = response.json()
        return data.get("runtime", 90)  # Default to 90 minutes if runtime is not found
    except requests.exceptions.RequestException as e:
        print(f"Error fetching runtime for movie {movie_id}: {e}")
        return 90  # Default value in case of an error

def fetch_genres():
    """
    Fetch the list of genres from TMDB and store them in a dictionary.
    Returns a dictionary mapping genre IDs to genre names.
    """
    try:
        response = requests.get(TMDB_GENRES_URL, params={"api_key": TMDB_API_KEY, "language": "fr-FR"})
        response.raise_for_status()
        genres_data = response.json()
        
        # Transform the list of genres into a dictionary {id: name}
        genre_dict = {genre["id"]: genre["name"] for genre in genres_data.get("genres", [])}
        return genre_dict

    except requests.exceptions.RequestException as e:
        print(f"Error fetching genres: {e}")
        return {}

@shared_task
def fetch_and_store_movies():
    """
    Fetch the currently playing movies from TMDB and store them in the database.
    If a movie already exists in the database, it will not be added again.
    """
    try:
        # Fetch the mapping of genre IDs to genre names
        genre_mapping = fetch_genres()

        if not genre_mapping:
            print("Warning: No genres retrieved, movies will be saved with IDs instead of names.")

        # Define parameters for the TMDB API request
        params = {
            "api_key": TMDB_API_KEY,
            "language": "fr-FR",
            "page": 1,
            "region": "CH"
        }
        response = requests.get(TMDB_NOW_PLAYING_URL, params=params)
        response.raise_for_status()
        data = response.json()

        # Ensure the 'results' key exists in the API response
        if 'results' not in data:
            raise ValueError("Key 'results' missing in TMDB response")

        # Limit the number of movies to process to 10
        movies = data['results'][:10]

        for movie in movies:
            # Extract movie details from the API response
            api_id = movie.get("id")
            title = movie.get("title", "Unknown Title")
            synopsis = movie.get("overview", "")[:500]
            genre_ids = movie.get("genre_ids", [])

            # Fetch the runtime of the movie
            duration = fetch_movie_runtime(api_id)

            # Convert genre IDs to genre names
            type_movie = ", ".join(genre_mapping.get(g, f"Unknown Genre ({g})") for g in genre_ids)

            release_date = movie.get("release_date", None)
            picture_url = f"https://image.tmdb.org/t/p/w500{movie.get('poster_path')}" if movie.get("poster_path") else ""
            rating = int(movie.get("vote_average", 0))

            # Parse the release date if it exists
            if release_date:
                try:
                    release_date = datetime.strptime(release_date, "%Y-%m-%d").date()
                except ValueError:
                    release_date = None

            # Check if the movie already exists in the database
            if not Movie.objects.filter(api_id=api_id).exists():
                # Create a new movie record in the database
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
                print(f"Movie added: {title} ({type_movie})")
            else:
                print(f"Movie already exists: {title}")

        return f"{len(movies)} movies successfully added"

    except requests.exceptions.RequestException as e:
        return f"TMDB request error: {str(e)}"
    except ValueError as e:
        return f"Data format error: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"
