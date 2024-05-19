from django.contrib.auth.backends import BaseBackend, ModelBackend
from passlib.hash import bcrypt as pass_cryptor
from .models import User


class MyBackend(BaseBackend):

    def authenticate(self, request, email=None, password=None):
        try:
            user = User.objects.get(email=email)
            if pass_cryptor.verify(password, user.password):
                return user
        except User.DoesNotExist:
            pass  # Gérer l'exception si l'utilisateur n'existe pas
        return None
