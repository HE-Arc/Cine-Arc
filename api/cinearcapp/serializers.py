from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Movie, Session, Basket, Room

User = get_user_model()  # use default user model

# Serializer User
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "password", "is_superuser"]

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)  # Hash password
        return user

# Serializer Movie
class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = "__all__"


# Serializer Room
class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"


# Serializer Session
class SessionSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)
    room = RoomSerializer(read_only=True)
    
    # Champs d'écriture pour les ID
    movie_id = serializers.PrimaryKeyRelatedField(
        queryset=Movie.objects.all(), source='movie', write_only=True)
    
    room_id = serializers.PrimaryKeyRelatedField(
        queryset=Room.objects.all(), source='room', write_only=True)

    class Meta:
        model = Session
        fields = ["id", "movie", "room", "movie_id", "room_id", "date_hour"]

# Serializer Basket
class BasketSerializer(serializers.ModelSerializer):
    session = SessionSerializer(read_only=True)
    user = UserSerializer(read_only=True)  # Affichage utilisateur

    # Champs pour l'ID de l'utilisateur et de la session
    session_id = serializers.PrimaryKeyRelatedField(
        queryset=Session.objects.all(), source='session', write_only=True)
    
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='user', write_only=True)

    class Meta:
        model = Basket
        fields = ["id", "session", "user", "quantity", "payed", "session_id", "user_id"]

    def validate_quantity(self, value):
        """Empêche une quantité négative ou nulle"""
        if value <= 0:
            raise serializers.ValidationError("La quantité doit être au moins 1.")
        return value