# filepath: d:\TroisiemeAnnee\Web_2\Cine-Arc\api\cinearcapp\backends.py
from django.contrib.auth.backends import BaseBackend
from .models import CustomUser

class EmailBackend(BaseBackend):
    """
    Custom authentication backend to authenticate users using their email and password.
    """
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(email=email)
            if user.check_password(password):
                return user
        except CustomUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None