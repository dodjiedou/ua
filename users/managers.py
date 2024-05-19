from django.contrib.auth.models import BaseUserManager

class UtilisateurManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Le nom d'utilisateur est requis")
        utilisateur = self.model(
            email=email,
        )
        
        utilisateur.set_password(password)
        utilisateur.save(using=self._db)
        return utilisateur

    def create_superuser(self, email, password=None):
        superuser = self.create_user(email, password)
        superuser.is_staff = True
        superuser.is_admin = True
        superuser.is_analyst = True
        superuser.is_superuser = True
        superuser.save(using=self._db)
        return superuser
