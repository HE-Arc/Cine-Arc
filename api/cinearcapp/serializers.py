from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Movie, Session, Basket, Room

# Get the default user model
User = get_user_model()

# Serializer for the User model
class UserSerializer(serializers.ModelSerializer):
    # Password field is write-only and styled as a password input
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "password", "is_superuser"]

    def create(self, validated_data):
        # Create a user with a hashed password
        user = User.objects.create_user(**validated_data)
        return user

# Serializer for the Movie model
class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = "__all__"  # Include all fields from the Movie model

# Serializer for the Room model
class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"  # Include all fields from the Room model

# Serializer for the Session model
class SessionSerializer(serializers.ModelSerializer):
    # Nested serializers for movie and room (read-only)
    movie = MovieSerializer(read_only=True)
    room = RoomSerializer(read_only=True)
    
    # Write-only fields for movie and room IDs
    movie_id = serializers.PrimaryKeyRelatedField(
        queryset=Movie.objects.all(), source='movie', write_only=True)
    room_id = serializers.PrimaryKeyRelatedField(
        queryset=Room.objects.all(), source='room', write_only=True)

    class Meta:
        model = Session
        fields = ["id", "movie", "room", "movie_id", "room_id", "date_hour"]

# Serializer for the Basket model
class BasketSerializer(serializers.ModelSerializer):
    # Nested serializers for session and user (read-only)
    session = SessionSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    # Write-only fields for session and user IDs
    session_id = serializers.PrimaryKeyRelatedField(
        queryset=Session.objects.all(), source='session', write_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='user', write_only=True)

    class Meta:
        model = Basket
        fields = ["id", "session", "user", "quantity", "payed", "session_id", "user_id"]

    def validate_quantity(self, value):
        """Ensure the quantity is positive and greater than zero"""
        if value <= 0:
            raise serializers.ValidationError("La quantité doit être au moins 1.")  # Error message in French
        return value