import re
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Movie, Room, Session, Basket
from .serializers import UserSerializer, MovieSerializer, RoomSerializer, SessionSerializer, BasketSerializer
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import stripe
from django.conf import settings

# Récupérer le modèle User
User = get_user_model()

stripe.api_key = settings.STRIPE_SECRET_KEY
# =======================
# VIEWSETS
# =======================

class UserViewSet(viewsets.ModelViewSet):
    """
    CRUD pour les utilisateurs.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]  

    def perform_create(self, serializer):
        """ Hash le mot de passe avant de sauvegarder l'utilisateur """
        user = serializer.save()
        user.set_password(user.password)
        user.save()

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.AllowAny]

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [permissions.AllowAny]

class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    permission_classes = [permissions.AllowAny]

class BasketViewSet(viewsets.ModelViewSet):
    queryset = Basket.objects.all()
    serializer_class = BasketSerializer
    permission_classes = [permissions.AllowAny]

def get_payment_details(request, user_id):
    """
    Récupère le total à payer pour l'utilisateur en fonction des tickets non payés.
    """
    user = get_object_or_404(User, id=user_id)
    
    # Filtrer les paniers non payés
    cart_items = Basket.objects.filter(user_id=user.id, payed=False)

    if not cart_items.exists():
        return JsonResponse({"error": "Aucun billet à payer"}, status=400)

    # Calcul du total
    total_amount = sum(item.quantity * 16 for item in cart_items)  # Prix unique 16 CHF

    return JsonResponse({"total": total_amount})

def create_checkout_session(request, user_id):
    """
    Crée une session Stripe pour le paiement.
    """
    user = get_object_or_404(User, id=user_id)

    cart_items = Basket.objects.filter(user_id=user.id, payed=False).select_related("session")

    if not cart_items.exists():
        return JsonResponse({"error": "Aucun billet à payer"}, status=400)

    total_amount = sum(item.quantity * 16 for item in cart_items)  # Prix en CHF

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "chf",
                        "product_data": {"name": "Réservation cinéma"},
                        "unit_amount": total_amount * 100,  # Convertir CHF en centimes
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url=f"http://localhost:5173/payment/success",
            cancel_url=f"http://localhost:5173/payment/cancel",
        )

        return JsonResponse({"checkout_url": session.url})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def payment_success(request):
    """
    Met à jour le panier de l'utilisateur en mettant 'payed' à True.
    """
    try:
        user_id = request.user.id  # ✅ Récupérer user_id dynamiquement
        baskets = Basket.objects.filter(user_id=user_id, payed=False)

        if not baskets.exists():
            return JsonResponse({'message': 'Aucun panier à mettre à jour.'}, status=404)

        baskets.update(payed=True)  # ✅ Mettre à jour tous les paniers non payés

        return JsonResponse({'message': 'Paiement confirmé, paniers mis à jour avec succès.'})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def payment_cancel(request):
    """
    Réponse lorsqu'un paiement est annulé par l'utilisateur.
    """
    return JsonResponse({'message': 'Paiement annulé, panier inchangé.'})
  
# =======================
# AUTHENTIFICATION
# =======================

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    Endpoint pour enregistrer un nouvel utilisateur avec validation du mot de passe.
    """
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")

    # Vérification des champs requis
    if not username or not email or not password:
        return Response({"error": "Tous les champs sont requis."}, status=status.HTTP_400_BAD_REQUEST)

    # Vérification de l'existence de l'email
    if User.objects.filter(email=email).exists():
        return Response({"error": "Un utilisateur avec cet email existe déjà."}, status=status.HTTP_400_BAD_REQUEST)

    # Vérification du mot de passe
    password_error = is_valid_password(password)
    if password_error:
        return Response({"error": password_error}, status=status.HTTP_400_BAD_REQUEST)

    # Création de l'utilisateur
    user = User.objects.create_user(username=username, email=email, password=password)

    return Response({"message": "Compte créé avec succès. Vous pouvez maintenant vous connecter."}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """
    Endpoint pour authentifier un utilisateur et renvoyer un token JWT.
    """
    email = request.data.get("email")
    password = request.data.get("password")

    if not email or not password:
        return Response({"error": "Email et mot de passe requis"}, status=status.HTTP_400_BAD_REQUEST)

    # Vérifier si l'utilisateur existe
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"error": "Utilisateur introuvable"}, status=status.HTTP_404_NOT_FOUND)

    # Authentifier avec son username car Django utilise username par défaut
    user = authenticate(username=user.username, password=password)
    if user is None:
        return Response({"error": "Mot de passe incorrect"}, status=status.HTTP_401_UNAUTHORIZED)

    # Générer un token JWT avec SimpleJWT
    refresh = RefreshToken.for_user(user)
    return Response({
        "refresh": str(refresh),
        "access": str(refresh.access_token),
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    """
    Récupère les infos de l'utilisateur connecté.
    """
    user = request.user
    return Response({'id': user.id, 'username': user.username, 'email': user.email})

def is_valid_password(password):
    """
    Vérifie si le mot de passe a au moins :
    - 8 caractères
    - 1 caractère spécial parmi (!@#$%^&*())
    """
    if len(password) < 8:
        return "Le mot de passe doit contenir au moins 8 caractères."

    if not re.search(r"[!@#$%^&*()]", password):
        return "Le mot de passe doit contenir au moins un caractère spécial (!@#$%^&*())."

    return None  # Aucun problème
