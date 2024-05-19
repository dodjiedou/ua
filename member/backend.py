
from django.contrib.auth.backends import BaseBackend, ModelBackend
from passlib.hash import bcrypt 
from passlib.hash import pbkdf2_sha256 
from users.models import Member
from django.contrib.auth.hashers import make_password, check_password

class MyBackend(BaseBackend):

    def authenticate(self, request, email=None, password=None):

        user = Member.objects.filter(email=email)

        if user.exists():

            # if bcrypt.verify(password, user.first().password):
            if check_password(password, user.first().password):
            # if user.first().password==password:

                return user.first()
            else:
                return None
        else:
            return None

    def get_user(self, user_id):
        try:
            return Member.objects.get(pk=user_id)
        except Member.DoesNotExist:
            return None