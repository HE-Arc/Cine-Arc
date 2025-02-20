from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Movie, Session, Reservation, Basket

User = get_user_model()

# --- Serializer pour les utilisateurs ---
User = get_user_model()  # Utiliser le modèle User par défaut de Django

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})  # Champ masqué en saisie

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)  # Hash automatiquement le mot de passe
        return user


# --- Serializer pour les films ---
class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ["id", "title", "synopsis", "duration", "type", "release_date", "picture_url", "rating"]

# --- Serializer pour les séances ---
class SessionSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)  # Inclut les détails du film lié

    class Meta:
        model = Session
        fields = ["id", "movie", "room", "date_hour"]

# --- Serializer pour les réservations ---
class ReservationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Inclut les détails de l'utilisateur
    #session = SessionSerializer(read_only=True)  # Inclut les détails de la séance

    class Meta:
        model = Reservation
        fields = ["id", "user", "total_amount", "date", "payment_status"]

# --- Serializer pour le panier ---
class BasketSerializer(serializers.ModelSerializer):
    session = SessionSerializer(read_only=True)  # Inclut les détails de la séance
    user = UserSerializer(read_only=True)  # Inclut les détails de l'utilisateur

    class Meta:
        model = Basket
        fields = ["session", "user", "quantity"]
        unique_together = ("session", "user")  # Empêche un utilisateur d'avoir plusieurs entrées pour la même session

    def validate_quantity(self, value):
        """Empêche une quantité négative ou nulle"""
        if value <= 0:
            raise serializers.ValidationError("La quantité doit être au moins 1.")
        return value
