from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import login_user, get_user_info, register_user
from rest_framework_simplejwt.views import TokenRefreshView

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
    path('auth/login/', login_user, name='login'),
    path('auth/user/', get_user_info, name='user_info'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("auth/register/", register_user, name="register_user"),
]
