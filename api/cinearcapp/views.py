from rest_framework import viewsets, permissions, serializers
from rest_framework.exceptions import ValidationError
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
from .models import Movie, Room, Session, Basket
from .serializers import UserSerializer, MovieSerializer, RoomSerializer, SessionSerializer, BasketSerializer
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import stripe
from django.conf import settings

# Get the default User model
User = get_user_model()

stripe.api_key = settings.STRIPE_SECRET_KEY

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

def get_current_user(request):
    """Renvoie les informations de l'utilisateur authentifié"""
    user = request.user
    return JsonResponse({"id": user.id, "username": user.username, "email": user.email})

def payment_cancel(request):
    """
    Réponse lorsqu'un paiement est annulé par l'utilisateur.
    """
    return JsonResponse({'message': 'Paiement annulé, panier inchangé.'})