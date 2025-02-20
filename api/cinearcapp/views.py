from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Movie, Session, Reservation, Basket
from .serializers import (
    UserSerializer, MovieSerializer, SessionSerializer, 
    ReservationSerializer, BasketSerializer
)

# --- Utilisateurs ---
User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# --- Films ---
class MovieList(APIView):
    def get(self, request, format=None):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

# --- Séances ---
class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer

# --- Réservations ---
class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    @action(detail=True, methods=["POST"], url_path="cancel")
    def cancel_reservation(self, request, pk):
        reservation = get_object_or_404(Reservation, pk=pk)

        # Simule l'annulation d'une réservation
        reservation.paiement_status = "not paid"
        reservation.save()

        return Response({"message": "Réservation annulée"}, status=status.HTTP_200_OK)

# --- Panier ---
class BasketViewSet(viewsets.ModelViewSet):
    queryset = Basket.objects.all()
    serializer_class = BasketSerializer

    @action(detail=True, methods=["POST"], url_path="increase-quantity")
    def increase_quantity(self, request, pk):
        basket_item = get_object_or_404(Basket, pk=pk)

        data = {"quantity": basket_item.quantity + 1}
        serializer = self.get_serializer(basket_item, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
