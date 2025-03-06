from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

# Modèle des Films
class Movie(models.Model):
    title = models.CharField(max_length=100)
    synopsis = models.CharField(max_length=500)
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
    

    def save(self,*args, **kwargs):
        if not self.pk:
            self.available_seats = self.room.capacity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.movie.title} - {self.room.name} ({self.date_hour})"

# Modèle du Panier
class Basket(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="baskets")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="baskets")
    quantity = models.IntegerField()
    payed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} - {self.session.movie.title} ({self.quantity})"
    
# Modèle de l'utilisateur    
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Crée un utilisateur avec un email et un mot de passe.
        """
        if not email:
            raise ValueError("L'email est obligatoire")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Crée un superutilisateur.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None  # Supprime le champ username
    email = models.EmailField(unique=True)  # Rend l'email obligatoire et unique

    USERNAME_FIELD = "email"  # Utilisation de l'email comme identifiant unique
    REQUIRED_FIELDS = []  # Pas besoin de username

    objects = CustomUserManager()  # Associe le nouveau UserManager

    def __str__(self):
        return self.email  # Affiche l'email au lieu du username
