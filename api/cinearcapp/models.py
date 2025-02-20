from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User

# Modèle des Films
class Movie(models.Model):
    title = models.CharField(max_length=100)
    synopsis = models.CharField(max_length=100)
    duration = models.IntegerField()
    type = models.CharField(max_length=50)
    release_date = models.DateField()
    picture_url = models.CharField(max_length=255)
    rating = models.IntegerField()
    api_id = models.IntegerField(unique=True)

    def __str__(self):
        return self.title

# Modèle des Salles
class Room(models.Model):
    capacity = models.IntegerField()
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# Modèle des Séances
class Session(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="sessions")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="sessions")
    date_hour = models.DateTimeField()

    def __str__(self):
        return f"{self.movie.title} - {self.room.name} ({self.date_hour})"

# Modèle du Panier
class Basket(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="baskets")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="baskets")
    quantity = models.IntegerField()
    payed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} - {self.session.movie.title} ({self.quantity})"
