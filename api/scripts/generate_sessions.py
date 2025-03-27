import json
import random
import os
import django
from datetime import datetime, timedelta

# Charger Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cinearc.settings")  # Mets ici le bon nom de ton projet Django
django.setup()

from cinearcapp.models import Movie, Room

# Vérifier que le dossier `fixtures/` existe
os.makedirs("cinearcapp/fixtures", exist_ok=True)

# Récupérer les films et salles stockés en base
movies = list(Movie.objects.all())
rooms = list(Room.objects.all())

# Vérifier qu'on a bien des films et des salles
if not movies or not rooms:
    print("Aucune donnée de film ou salle trouvée en base.")
    exit()

# Générer des séances uniques en associant films et salles aléatoirement
sessions = []
used_combinations = set()  # Pour éviter les doublons film/salle

for i in range(min(5, len(movies), len(rooms))):  # Prendre au max 5 films et salles
    movie = random.choice(movies)
    room = random.choice(rooms)
    
    # Vérifier qu'on n'a pas déjà associé ce film à cette salle
    while (movie.id, room.id) in used_combinations:
        movie = random.choice(movies)
        room = random.choice(rooms)

    used_combinations.add((movie.id, room.id))  # Ajouter à l'ensemble des combinaisons utilisées

    # Générer une date dans les prochains jours
    date_hour = (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%dT%H:%M:%S")

    session = {
        "model": "cinearcapp.session",
        "pk": i + 1,
        "fields": {
            "movie": movie.id,
            "room": room.id,
            "date_hour": date_hour,
            "available_seats": room.capacity  # Ajout de available_seats basé sur la capacité de la salle
        }
    }
    sessions.append(session)

# Sauvegarde dans `sessions.json`
fixture_path = "cinearcapp/fixtures/sessions.json"
with open(fixture_path, "w", encoding="utf-8") as f:
    json.dump(sessions, f, indent=4)

print(f"La fixture `{fixture_path}` a été générée avec {len(sessions)} séances.")
