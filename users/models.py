from django.db import models
from django.contrib.auth.models import  AbstractBaseUser, PermissionsMixin
from .managers import UtilisateurManager
from django_countries.fields import CountryField
from focalpoint.models import *


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='addresse email', max_length=255, unique=True,)
    nom=models.CharField(max_length=255)
    prenom=models.CharField(max_length=255)
    departement=models.CharField(max_length=255)
    telephone=models.CharField(null=True, max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) # a admin user; non super-user
    is_admin = models.BooleanField(default=False) # a superuser 
    is_analyst = models.BooleanField(default=False)
    # remarquez l'absence du "champ password", c'est intégré pas besoin de preciser.
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Email & Password sont requis par défaut.
    def get_full_name(self):
        # L'utilisateur est identifié par son adresse e-mail
        return f'{self.prenom} {self.nom}'
    
    def get_initials(self):
        return f"{self.nom[:1].upper()}{self.prenom[:1].lower()}"
    
    def get_short_name(self):
        # L'utilisateur est identifié par son adresse e-mail
        return self.email
    
    def __str__(self):
        return self.email
    
    objects = UtilisateurManager()


class Member(User):
    focal_point = models.ForeignKey(FocalPoint, on_delete=models.CASCADE)
    country = CountryField(null=True, blank=True)
    city = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    phone = models.CharField(null= True, max_length=100)
    created_at = models.DateTimeField(null=True,auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    photo = models.TextField(null=True)

class Commentaire(models.Model):
    membre = models.ForeignKey(Member, on_delete=models.CASCADE)
    article = models.ForeignKey(Information, on_delete=models.CASCADE)
    commentaire = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)


class Alerte(models.Model):
    title = models.CharField(blank=False,null=True, max_length=255)
    membre = models.ForeignKey(Member, on_delete=models.CASCADE)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name='alertes')
    #categorie = models.CharField(blank=False,null=True, max_length=255)
    is_published = models.BooleanField(default=False)
    contenu = models.TextField()
    file = models.FileField(null=True,blank=True, upload_to='member/alerte')
    date_creation = models.DateTimeField(auto_now_add=True)


class Like(models.Model,):
    membre = models.ForeignKey(Member, on_delete=models.CASCADE)
    article = models.ForeignKey(Information, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)