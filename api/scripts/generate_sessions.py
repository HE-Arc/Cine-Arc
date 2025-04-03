import json
import random
import os
import django
from datetime import datetime, timedelta

# Load Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cinearc.settings")  # Replace with your Django project name
django.setup()

from cinearcapp.models import Movie, Room

# Ensure the `fixtures/` directory exists
os.makedirs("cinearcapp/fixtures", exist_ok=True)

# Retrieve movies and rooms from the database
movies = list(Movie.objects.all())
rooms = list(Room.objects.all())

# Check if there are movies and rooms in the database
if not movies or not rooms:
    print("No movie or room data found in the database.")
    exit()

# Generate unique sessions by randomly associating movies and rooms
sessions = []
used_combinations = set()  # To avoid duplicate movie/room combinations

for i in range(min(5, len(movies), len(rooms))):  # Limit to a maximum of 5 sessions
    movie = random.choice(movies)
    room = random.choice(rooms)
    
    # Ensure the movie/room combination is unique
    while (movie.id, room.id) in used_combinations:
        movie = random.choice(movies)
        room = random.choice(rooms)

    used_combinations.add((movie.id, room.id))  # Mark the combination as used

    # Generate a session date in the upcoming days
    date_hour = (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%dT%H:%M:%S")

    session = {
        "model": "cinearcapp.session",  # Specify the model for the fixture
        "pk": i + 1,  # Primary key for the session
        "fields": {
            "movie": movie.id,  # Movie ID
            "room": room.id,  # Room ID
            "date_hour": date_hour,  # Date and time of the session
            "available_seats": room.capacity  # Available seats based on room capacity
        }
    }
    sessions.append(session)

# Save the generated sessions to `sessions.json`
fixture_path = "cinearcapp/fixtures/sessions.json"
with open(fixture_path, "w", encoding="utf-8") as f:
    json.dump(sessions, f, indent=4)
