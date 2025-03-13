from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
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
        

@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    """
    Authentifie un utilisateur avec son email et renvoie un token JWT.
    """
    email = request.data.get("email")  # Utiliser `email` au lieu de `username`
    password = request.data.get("password")

    user = User.objects.filter(email=email).first()  # Rechercher l'utilisateur par email

    if user and user.check_password(password):  # Vérifier le mot de passe
        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "email": user.email
        })
    else:
        return Response({"error": "Identifiants incorrects"}, status=400)



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

# Basket ViewSet
class BasketViewSet(viewsets.ModelViewSet):
    """
    Handles CRUD operations for baskets.
    Only authenticated users can access and create a basket.
    """
    queryset = Basket.objects.all()
    serializer_class = BasketSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can access

    def perform_create(self, serializer):
        """
        Automatically assigns the logged-in user to the basket.
        """
        serializer.save(user=self.request.user)
