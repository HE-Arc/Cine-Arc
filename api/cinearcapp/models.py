from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User

# Model for Movies
class Movie(models.Model):
    title = models.CharField(max_length=100)  # Title of the movie
    synopsis = models.CharField(max_length=500)  # Short description of the movie
    duration = models.IntegerField()  # Duration of the movie in minutes
    type = models.CharField(max_length=50)  # Genre or type of the movie
    release_date = models.DateField()  # Release date of the movie
    picture_url = models.CharField(max_length=255)  # URL of the movie poster or image
    rating = models.IntegerField()  # Rating of the movie (e.g., out of 10)
    api_id = models.IntegerField(unique=True)  # Unique identifier for the movie from an external API

    def __str__(self):
        return self.title  # String representation of the movie (its title)

# Model for Rooms
class Room(models.Model):
    capacity = models.IntegerField()  # Maximum seating capacity of the room
    name = models.CharField(max_length=50)  # Name of the room

    def __str__(self):
        return self.name  # String representation of the room (its name)

# Model for Sessions
class Session(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="sessions")  # Movie being shown in the session
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="sessions")  # Room where the session is held
    date_hour = models.DateTimeField()  # Date and time of the session

    def save(self, *args, **kwargs):
        # If the session is being created for the first time, set available seats to the room's capacity
        if not self.pk:
            self.available_seats = self.room.capacity
        super().save(*args, **kwargs)  # Call the parent class's save method

    def __str__(self):
        # String representation of the session (movie title, room name, and date/time)
        return f"{self.movie.title} - {self.room.name} ({self.date_hour})"

# Model for Basket
class Basket(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="baskets")  # Session associated with the basket
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="baskets")  # User who owns the basket
    quantity = models.IntegerField()  # Number of tickets in the basket
    payed = models.BooleanField(default=False)  # Whether the basket has been paid for

    def __str__(self):
        # String representation of the basket (user email, movie title, and quantity)
        return f"{self.user.email} - {self.session.movie.title} ({self.quantity})"
