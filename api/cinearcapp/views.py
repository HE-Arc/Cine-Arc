import re
import os
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
import time
from django.utils.text import slugify

# Get the User model
User = get_user_model()

# Environment variables for frontend URL and Stripe secret key
FRONTEND_URL = os.getenv("FRONTEND_URL")
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# =======================
# VIEWSETS
# =======================

class UserViewSet(viewsets.ModelViewSet):
    """
    CRUD operations for users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]  

    def perform_create(self, serializer):
        """
        Hash the password before saving the user.
        """
        user = serializer.save()
        user.set_password(user.password)
        user.save()

class MovieViewSet(viewsets.ModelViewSet):
    """
    CRUD operations for movies.
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.AllowAny]

class RoomViewSet(viewsets.ModelViewSet):
    """
    CRUD operations for rooms.
    """
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [permissions.AllowAny]

class SessionViewSet(viewsets.ModelViewSet):
    """
    CRUD operations for sessions.
    """
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    permission_classes = [permissions.AllowAny]

class BasketViewSet(viewsets.ModelViewSet):
    """
    Handles CRUD operations for shopping baskets.
    """
    serializer_class = BasketSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can access

    def get_queryset(self):
        """
        Retrieve only the baskets of the logged-in user that are not paid.
        """
        return Basket.objects.filter(user=self.request.user, payed=False)

    def perform_create(self, serializer):
        """
        Automatically assign the basket to the logged-in user when an item is added.
        """
        serializer.save(user=self.request.user)

# =======================
# PAYMENT
# =======================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def create_checkout_session(request):
    """
    Create a Stripe session for payment.
    """
    user = request.user  # Get the logged-in user using the token

    # Retrieve unpaid cart items for the user
    cart_items = Basket.objects.filter(user=user, payed=False).select_related("session")

    if not cart_items.exists():
        return Response({"error": "No tickets to pay for"}, status=400)

    # Calculate the total amount in CHF
    total_amount = sum(item.quantity * 16 for item in cart_items)

    try:
        # Create a Stripe checkout session
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "chf",
                        "product_data": {"name": "Cinema Reservation"},
                        "unit_amount": total_amount * 100,  # Convert CHF to cents
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url=f"{FRONTEND_URL}/payment/success",
            cancel_url=f"{FRONTEND_URL}/payment/cancel",
        )

        return Response({"checkout_url": session.url})

    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def payment_success(request):
    """
    Update the user's basket by setting 'payed' to True after successful payment.
    """
    user = request.user  # Get the user from the token
    
    try:
        # Retrieve all unpaid baskets for the user
        baskets = Basket.objects.filter(user=user)
        
        if not baskets.exists():
            return Response({'message': 'No basket to update.'}, status=404)

        # Update each basket
        baskets.update(payed=True)

        return Response({'message': 'Payment confirmed, basket updated successfully.'}, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

def payment_cancel(request):
    """
    Response when a payment is canceled by the user.
    """
    return JsonResponse({'message': 'Payment canceled, basket unchanged.'})
  
# =======================
# AUTHENTICATION
# =======================

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    Endpoint to register a new user with password validation.
    """
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")

    # Check required fields
    if not username or not email or not password:
        return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

    # Check if the email already exists
    if User.objects.filter(email=email).exists():
        return Response({"error": "A user with this email already exists."}, status=status.HTTP_400_BAD_REQUEST)

    # Validate the password
    password_error = is_valid_password(password)
    if password_error:
        return Response({"error": password_error}, status=status.HTTP_400_BAD_REQUEST)
    
    # If the username already exists, make it unique (slugified + timestamp)
    if User.objects.filter(username=username).exists():
        base = slugify(username)
        username = f"{base}_{int(time.time())}"

    # Create the user
    user = User.objects.create_user(username=username, email=email, password=password)

    return Response({"message": "Account successfully created. You can now log in."}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """
    Endpoint to authenticate a user and return a JWT token.
    """
    email = request.data.get("email")
    password = request.data.get("password")

    if not email or not password:
        return Response({"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

    # Check if the user exists
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    # Authenticate using the username since Django uses username by default
    user = authenticate(username=user.username, password=password)
    if user is None:
        return Response({"error": "Incorrect password"}, status=status.HTTP_401_UNAUTHORIZED)

    # Generate a JWT token using SimpleJWT
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
    Retrieve information about the logged-in user.
    """
    user = request.user
    return Response({'id': user.id, 'username': user.username, 'email': user.email, 'is_superuser': user.is_superuser})

def is_valid_password(password):
    """
    Check if the password meets the following criteria:
    - At least 8 characters
    - At least 1 special character from (!@#$%^&*())
    """
    if len(password) < 8:
        return "The password must be at least 8 characters long."

    if not re.search(r"[!@#$%^&*()]", password):
        return "The password must contain at least one special character (!@#$%^&*())."

    return None  # No issues with the password
