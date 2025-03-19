from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Instanciation du Router de DRF
router = DefaultRouter()

# Enregistrement des ViewSets
router.register(r"users", views.UserViewSet, basename="user")
router.register(r"movies", views.MovieViewSet, basename="movie")
router.register(r"sessions", views.SessionViewSet, basename="session")
router.register(r"room", views.RoomViewSet, basename="room")
router.register(r"basket", views.BasketViewSet, basename="basket")

# Finalisation des urlpatterns
urlpatterns = [
    path("", include(router.urls)),  # Inclut toutes les URLs générées par le Router
    path("payment/<int:user_id>/", views.get_payment_details, name="get_payment_details"),
    path("payment/checkout/<int:user_id>/", views.create_checkout_session, name="create_checkout_session"),
    path("payment/success/", views.payment_success, name="payment_success"),  # 🚀 Suppression de user_id ici
    path("payment/cancel/", views.payment_cancel, name="payment_cancel"),  # Ajout d'une route d'annulation
    path("users/me/", views.get_current_user, name="current-user"),
]
