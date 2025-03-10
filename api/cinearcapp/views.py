from rest_framework import viewsets, permissions, serializers
from rest_framework.exceptions import ValidationError
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
from .models import Movie, Room, Session, Basket
from .serializers import UserSerializer, MovieSerializer, RoomSerializer, SessionSerializer, BasketSerializer

# Get the default User model
User = get_user_model()

# User ViewSet
class UserViewSet(viewsets.ModelViewSet):
    """
    This view handles CRUD operations for users.
    When creating a new user, the password is automatically hashed.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]  # Modify this as needed (IsAuthenticated, etc.)

    def perform_create(self, serializer):
        """
        Automatically hashes the password before saving the user.
        """
        user = serializer.save()
        user.set_password(user.password)  # Hash the password
        user.save()

# Movie ViewSet
class MovieViewSet(viewsets.ModelViewSet):
    """
    Handles CRUD operations for movies.
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.AllowAny]  # Anyone can access

# Room ViewSet
class RoomViewSet(viewsets.ModelViewSet):
    """
    Handles CRUD operations for rooms.
    """
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [permissions.AllowAny]

# Session ViewSet
class SessionViewSet(viewsets.ModelViewSet):
    """
    Handles CRUD operations for movie sessions.
    """
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    permission_classes = [permissions.AllowAny]

class BasketViewSet(viewsets.ModelViewSet):
    """
    Handles CRUD operations for baskets.
    """
    queryset = Basket.objects.all()
    serializer_class = BasketSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        """
        Assigne l'utilisateur "en dur" (ID 1) à chaque panier lors de sa création.
        """
        user_id = 1  # Utiliser l'utilisateur avec l'ID 1, ou obtenir l'utilisateur actuel via authentication
        session = serializer.validated_data.get('session')

        # Vous pouvez définir l'utilisateur en dur ici si vous ne faites pas de gestion d'authentification
        serializer.save(user_id=user_id, session=session)



